import mailchimp

api_key = "715edd2d3aba67e15f92d7fbd5ac4f13-us16"
list_id = "4e28f56bd8"

def get_mailchimp_api():
    return mailchimp.Mailchimp(api_key)

m = get_mailchimp_api()




email = {"": "join@cfe.com"}

m.lists.subscribe(
            list_id,
            email,
            double_optin=False,
            update_existing=False,
            send_welcome=False
            )
