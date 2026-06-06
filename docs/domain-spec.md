# Allugare — Domain Spec (extracted from the 2017 codebase)

> **Purpose.** This document distills the *durable knowledge* from the original
> Django 1.11 / Python 3.6 `allugare` app into a framework-agnostic spec you can
> hand to a fresh 2026 build. It captures **what** the product is, the **data
> model**, and the **business rules** — not the (obsolete) implementation.
>
> **Provenance legend** for every rule below:
> - 📦 **Extracted** — taken directly from the old code; this is encoded product knowledge.
> - 🔧 **Recommendation** — my advice for a 2026 build; *not* in the original.
> - ⚠️ **Gap** — something a real product needs that the original lacked.

---

## 1. What the product actually is

📦 **A student-housing & roommate marketplace for Brazil**, not a generic real
estate portal. Evidence baked into the schema:

- `Profile` carries `universidade` (university) and `curso` (degree/major).
- The bio prompt is literally *"Quem é você e com quem gostaria de morar?"*
  ("Who are you and who would you like to live with?").
- Facebook login requested the `user_friends` scope — social proof / finding
  housemates through your network.

Two-sided: **owners/sublessors** post rental listings (`Imovel`); **students**
browse, view listings, and contact each other. The detail page surfaces the
poster's Facebook name + photo as a trust signal.

🔧 Keep this framing front-and-center — "student housing in Brazil" drives very
different decisions than "general real estate" (price ranges, lease lengths,
roommate matching, university-proximity search, trust between strangers).

---

## 2. Core entities

### 2.1 `Imovel` (Property Listing) — the heart of the product

📦 Fields, grouped as the original form presented them. Portuguese field names
kept because they're domain terms; English glosses added.

**Ownership & status**
| Field | Type | Rules | Notes |
|---|---|---|---|
| `user` | FK → User | required | the lister/owner |
| `active` | bool | default `True` | "Anúncio Ativo" — listing visible/hidden toggle |

**Address (BR format)**
| Field | Type | Rules | Notes |
|---|---|---|---|
| `uf` | char(2) | required, choices | Brazilian state code (27 values, see §5) |
| `cidade` | char(120) | required | city |
| `bairro` | char(120) | required | neighborhood — primary search/display unit (it's the `__str__`) |
| `rua` | char(120) | required | street ("Rua, avenida, alameda") |
| `numero` | positive int | required | street number |
| `complemento` | char(120) | optional | apt/unit |
| `cep` | char(10) | required | postal code |
| `referencia` | char(120) | optional | landmark reference |

⚠️ Address is **free-text** — no validation, no CEP→address lookup, no geocoding
at write time. See §6.

**Property characteristics**
| Field | Type | Rules | Notes |
|---|---|---|---|
| `tipo_imovel` | char(20) | default `Casa`, choices | Casa, Apartamento, Kitnet, Edícula, Outro |
| `area_util` | positive int | optional | usable area in m² |
| `qtd_quartos` | positive int | required | bedrooms (form: 0–10) |
| `qtd_banheiros` | positive int | required | bathrooms (form: 0–10) |
| `qtd_vagas` | positive int | optional | parking spaces (form: 0–10) |
| `mobiliado` | bool | default `False` | furnished |
| `descricao` | text | optional | free description; hint: "Mobiliado, piscina, quintal…" |
| `video` | URL(200) | optional | external video tour link |

**Pricing (BR rental cost breakdown — this is the valuable part)**
| Field | Type | Rules | Notes |
|---|---|---|---|
| `preco_locacao` | decimal(8,2) | required | base rent ("Aluguel") |
| `preco_condominio` | decimal(8,2) | default 0 | HOA/building fee ("Condomínio") |
| `iptu` | decimal(8,2) | default 0 | **annual** property tax |
| `conta_agua` | decimal(8,2) | default 0 | water bill estimate |
| `conta_luz` | decimal(8,2) | default 0 | electricity bill estimate |
| `preco_total` | computed | — | see business rule BR-1 |

**Dates**
| Field | Type | Rules | Notes |
|---|---|---|---|
| `move_in_date` | date | default now | "Vago a partir de" — available-from |
| `timestamp` | date | auto on create | |
| `updates` | datetime | auto on update | listings ordered by `-timestamp, -updates` |

### 2.2 `ImovelPhotos` (Listing Photos)

📦
| Field | Type | Notes |
|---|---|---|
| `user` | FK → User | denormalized owner |
| `imovel` | FK → Imovel | parent listing |
| `order` | positive int | manual gallery ordering (drag-to-order) |
| `width` / `height` | int | cached image dimensions |
| `photos` | image | stored at `{user}/{imovel}/{filename}` on S3 |

Uploaded via a Django formset supporting add / reorder / delete in one screen.
⚠️ No max-count, no thumbnailing, no moderation, raw originals served from S3.

### 2.3 `Profile` (User Profile) — auto-created per user

📦 One-to-one with User. **Auto-created via a `post_save` signal** the moment a
User is created (BR-2).
| Field | Type | Notes |
|---|---|---|
| `profilePic` (+ `width`/`height`) | image | stored at `{user}/Profile/{filename}` |
| `nome` | char(120) | full name |
| `universidade` | char(120) | **university** — student-housing signal |
| `curso` | char(120) | **degree/major** |
| `uf` | char(2) | state (choices) |
| `cidade` | char(120) | city |
| `telefone` | char(20) | contact phone — **explicitly private** ("não estará visível para outros usuários") |
| `bio` | text | "Quem é você e com quem gostaria de morar?" |

🔧 Note the **phone-is-private** rule — contact happens in-app, not by exposing
numbers. Preserve that; it's a trust/safety decision.

### 2.4 `Message` / "Anúncio" (mensagens app) — ⚠️ half-baked

📦 The `mensagens.Message` model is **not** real user-to-user messaging despite
the name. It's a thin "announcement" record: `user`, `anuncio` (char(140),
**unique**), `mensagem` (text ≤5000), timestamps. The unique constraint on a
140-char title is a design smell.

📦 Actual inboxing was delegated to the third-party `django_messages` package
(see `INSTALLED_APPS` + the `inbox` context processor), separate from this model.

🔧 **Don't port this.** Design a proper threaded-conversation model from scratch
(see §6). The only takeaway: *the product needs in-app messaging between a
prospective tenant and a lister, scoped to a specific listing.*

### 2.5 `UserSession` (analytics app)

📦 On every login (`user_logged_in` signal), records `user`, `session_key`,
`ip_address`, and **GeoIP-resolved `city` / `country`** (via bundled MaxMind
GeoLite2 `.mmdb` files), plus raw `city_data` JSON. Used for basic "where are our
users" analytics.

🔧 Reasonable concept; in 2026 use a hosted GeoIP/analytics service or keep
MaxMind but **don't commit the `.mmdb` files** and respect LGPD (BR privacy law)
— IP + location is personal data.

### 2.6 `LandingPage` (landing app) — pre-launch lead capture

📦 A waitlist/lead form: `nome_completo`, `email`, `telefone`, `caracteristicas`
(free-text "what are you looking for — # bedrooms, price range, etc."),
`timestamp`. This was a demand-capture form before/around launch.

---

## 3. Business rules

- **BR-1 — Total monthly cost.** 📦 The headline domain rule:
  ```
  preco_total = preco_locacao + preco_condominio + (iptu / 12)
  ```
  IPTU is an **annual** tax, so it's amortized to a monthly figure. Tenants
  compare the *all-in* monthly number, not base rent.
  ⚠️ The original **excludes** `conta_agua` and `conta_luz` from the total (a
  prior version included them — see the commented-out line). 🔧 Decide
  deliberately: show an "all-in" total *and* an itemized breakdown; make clear
  which utilities are included vs. estimated.

- **BR-2 — Profile auto-provisioning.** 📦 Creating a User auto-creates an empty
  `Profile` (signal). 🔧 Keep the guarantee "every user has a profile," but
  prefer `get_or_create` in a transaction over a signal that silently swallows
  errors (the original wraps it in a bare `except: pass`).

- **BR-3 — Listing visibility.** 📦 `active` toggles whether a listing shows.
  ⚠️ The original list view does **not** filter on `active` — inactive listings
  still appear. 🔧 Public queries must filter `active=True`.

- **BR-4 — Ordering.** 📦 Listings and messages sort by `-timestamp, -updates`
  (newest first). Photos sort by manual `order`.

- **BR-5 — Trust signal.** 📦 Listing detail page pulls the lister's Facebook
  name + profile photo to humanize the poster. 🔧 Re-implement as a generic
  "verified identity" badge (Facebook's that API is dead); the *intent* —
  show who you'd be renting from — is sound.

- **BR-6 — Contact privacy.** 📦 Phone numbers are collected but never shown to
  other users. Contact is mediated in-app.

---

## 4. Feature surface (routes → capability)

📦 Extracted from URLconf:

| Capability | Original route |
|---|---|
| Home / about | `/`, `/sobre` |
| Auth (login, signup, social) | `/accounts/…` (allauth) |
| Browse listings (paginated, 20/page) | `/lares/` |
| View listing detail (+map, +lister FB) | `/lares/<pk>/` |
| Create listing | `/lares/create/` |
| Edit / delete listing | `/lares/<pk>/update/`, `/delete/` |
| Manage listing photos (add/reorder/delete) | `/lares/<pk>/photos/` |
| View / edit own profile | `/profiles/<username>/`, `/update/` |
| Messages / announcements | `/mensagens/…` |
| Waitlist lead form | `/land/contact/` |

🔧 This is the MVP feature list. A 2026 build adds search/filter, map-bounds
search, saved searches, and real messaging (see §6).

---

## 5. Brazil-specific reference data

📦 **`UF` — 27 state codes** (hardcoded in the original, duplicated in 3 files —
🔧 define once):
```
AC AL AP AM BA CE DF ES GO MA MG MS MT PA PB PR PE PI RJ RN RO RR RS SC SP SE TO
```

📦 **`tipo_imovel`:** Casa, Apartamento, Kitnet, Edícula, Outro.
🔧 Consider adding: Quarto (single room — core to student housing!), República,
Studio/Loft.

📦 **Currency:** BRL, `R$` prefix, `decimal(8,2)` (caps a value at 999,999.99 —
fine for rent, fine to keep).

🔧 **CEP** (postal code): integrate a CEP lookup (e.g. ViaCEP) to auto-fill
bairro/cidade/uf and validate format `00000-000`.

---

## 6. What a 2026 build needs that the original lacked (⚠️ gaps)

These are the genuinely hard parts of a listings product — none existed in the
original, so don't let it scope you short:

1. **Geospatial search.** PostGIS from day one. Geocode addresses *at write time*
   (not per page render). Support "within X km of a university / map bounds."
   The original geocoded synchronously inside the detail view with a hardcoded
   Google key — do not repeat.
2. **Structured, validated addresses.** CEP lookup + normalized
   address/lat-lng, not free-text CharFields.
3. **Search & filtering at scale.** Full-text + faceted filters (price range,
   bedrooms, type, furnished, neighborhood, university proximity). A bare
   paginated list doesn't survive real inventory.
4. **Real messaging.** Threaded conversations scoped to a listing, between two
   users, with read state and notifications. Replace both the half-baked
   `Message` model and the `django_messages` dependency.
5. **Image pipeline.** Upload → validate → thumbnail/responsive variants → CDN,
   with per-listing limits and basic moderation.
6. **Object-level authorization.** The original let any logged-in user edit/
   delete *any* listing (no owner check on update/delete/photos). Owner-scope
   every mutating query.
7. **Trust & safety.** Identity verification, listing moderation, report/abuse
   flows, spam controls — critical for strangers arranging housing.
8. **Privacy/LGPD.** IP + geolocation + contact data are personal data under
   Brazilian law; handle consent, retention, and deletion deliberately.
9. **Roommate matching (product opportunity).** The student angle +
   "who would you like to live with?" bio hint at a matching feature the
   original never built. Worth a product conversation.

---

## 7. One-paragraph summary for a fresh project

Build a **student-housing rental marketplace for Brazil**. Owners post listings
(`Imovel`) with a BR-specific cost breakdown — rent + condomínio + monthly-
amortized IPTU + utilities — full address, characteristics (type, bedrooms,
bathrooms, parking, furnished, area), an availability date, photos, and an
optional video. Students have profiles tied to their university and course, a
private contact phone, and a "who I'd like to live with" bio. Browsing,
listing detail with a trust signal for the lister, in-app messaging scoped to a
listing, and login-time geo analytics round out the MVP. Net-new for 2026:
PostGIS-backed proximity/search, validated CEP addresses, a real image pipeline,
threaded messaging, object-level authorization, LGPD compliance, and an optional
roommate-matching feature the original only hinted at.
