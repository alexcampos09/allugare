# -*- coding: utf-8 -*-
"""Seed demo data so the app looks populated for screenshots / client demos.

Idempotent: creates an admin user, a demo owner, and a handful of property
listings (imoveis). Safe to run repeatedly.

    python manage.py seed_demo
"""
from __future__ import unicode_literals

from decimal import Decimal

from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site
from django.core.management.base import BaseCommand

from allauth.socialaccount.models import SocialApp
from lares.models import Imovel

User = get_user_model()

DEMO_LISTINGS = [
    {
        "uf": "SP", "cidade": "São Paulo", "bairro": "Vila Madalena",
        "rua": "Rua Harmonia", "numero": 321, "cep": "05435-000",
        "tipo_imovel": "Apartamento", "area_util": 68,
        "qtd_quartos": 2, "qtd_banheiros": 1, "qtd_vagas": 1, "mobiliado": True,
        "descricao": "Apartamento charmoso a poucos passos dos bares e cafés da Vila.",
        "preco_locacao": Decimal("2800.00"), "preco_condominio": Decimal("650.00"),
        "iptu": Decimal("120.00"),
    },
    {
        "uf": "SP", "cidade": "São Paulo", "bairro": "Pinheiros",
        "rua": "Rua dos Pinheiros", "numero": 1180, "cep": "05422-001",
        "tipo_imovel": "Studio", "area_util": 38,
        "qtd_quartos": 1, "qtd_banheiros": 1, "qtd_vagas": 0, "mobiliado": True,
        "descricao": "Studio compacto e bem iluminado, ideal para quem trabalha na região.",
        "preco_locacao": Decimal("2100.00"), "preco_condominio": Decimal("480.00"),
        "iptu": Decimal("90.00"),
    },
    {
        "uf": "RJ", "cidade": "Rio de Janeiro", "bairro": "Botafogo",
        "rua": "Rua Voluntários da Pátria", "numero": 45, "cep": "22270-000",
        "tipo_imovel": "Casa", "area_util": 140,
        "qtd_quartos": 3, "qtd_banheiros": 2, "qtd_vagas": 2, "mobiliado": False,
        "descricao": "Casa espaçosa com quintal, perto da enseada e do metrô.",
        "preco_locacao": Decimal("4500.00"), "preco_condominio": Decimal("0.00"),
        "iptu": Decimal("260.00"),
    },
    {
        "uf": "MG", "cidade": "Belo Horizonte", "bairro": "Savassi",
        "rua": "Rua Pernambuco", "numero": 1024, "cep": "30130-151",
        "tipo_imovel": "Apartamento", "area_util": 95,
        "qtd_quartos": 3, "qtd_banheiros": 2, "qtd_vagas": 1, "mobiliado": False,
        "descricao": "Amplo apartamento no coração da Savassi, com varanda.",
        "preco_locacao": Decimal("3200.00"), "preco_condominio": Decimal("720.00"),
        "iptu": Decimal("180.00"),
    },
    {
        "uf": "PR", "cidade": "Curitiba", "bairro": "Batel",
        "rua": "Avenida do Batel", "numero": 760, "cep": "80420-090",
        "tipo_imovel": "Apartamento", "area_util": 110,
        "qtd_quartos": 3, "qtd_banheiros": 3, "qtd_vagas": 2, "mobiliado": True,
        "descricao": "Cobertura mobiliada com vista, no bairro mais badalado de Curitiba.",
        "preco_locacao": Decimal("5200.00"), "preco_condominio": Decimal("980.00"),
        "iptu": Decimal("340.00"),
    },
]


class Command(BaseCommand):
    help = "Create an admin user, a demo owner, and sample property listings."

    def handle(self, *args, **options):
        admin, created = User.objects.get_or_create(
            username="admin",
            defaults={"email": "admin@allugare.local", "is_staff": True, "is_superuser": True},
        )
        if created:
            admin.set_password("admin")
            admin.save()
            self.stdout.write(self.style.SUCCESS("Created superuser admin / admin"))
        else:
            self.stdout.write("Superuser 'admin' already exists")

        owner, _ = User.objects.get_or_create(
            username="corretora",
            defaults={"email": "corretora@allugare.local"},
        )

        created_count = 0
        for data in DEMO_LISTINGS:
            _, was_created = Imovel.objects.get_or_create(
                rua=data["rua"], numero=data["numero"], cidade=data["cidade"],
                defaults=dict(data, user=owner),
            )
            created_count += int(was_created)

        # Dummy Facebook SocialApp so the login/signup templates (which
        # reference the provider directly) render without 500ing. Not usable
        # for real auth — placeholder credentials only.
        fb, fb_created = SocialApp.objects.get_or_create(
            provider="facebook",
            defaults={"name": "Facebook (demo)", "client_id": "demo", "secret": "demo"},
        )
        fb.sites.add(Site.objects.get_current())
        if fb_created:
            self.stdout.write("Created dummy Facebook SocialApp")

        self.stdout.write(self.style.SUCCESS(
            "Seed complete: %d new listing(s), %d total."
            % (created_count, Imovel.objects.count())
        ))
