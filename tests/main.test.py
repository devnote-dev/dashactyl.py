from ..dashactyl import Dashactyl

dash = Dashactyl('https://client.dynox.us', '$omeFak3AP1Key') # I'm not creative
print(dash.ping())

user = dash.users.get(622146791659405313) # that's me
print(user.tag)
