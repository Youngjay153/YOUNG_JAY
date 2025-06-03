from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
import requests

class MTNNetworkBlockerMobile(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 20
        self.spacing = 20

        self.title_label = Label(text="MTN Network Blocker", font_size='24sp', size_hint=(1, 0.3))
        self.add_widget(self.title_label)

        self.check_button = Button(text="Check Network", size_hint=(1, 0.3))
        self.check_button.bind(on_press=self.check_network)
        self.add_widget(self.check_button)

    def is_vpn(self):
        try:
            # Using ipapi.co to check if IP is a VPN or proxy
            response = requests.get("https://ipapi.co/json/")
            if response.status_code == 200:
                data = response.json()
                # ipapi.co returns 'proxy' key to indicate VPN or proxy usage
                return data.get('proxy', False)
            else:
                self.show_popup("Error", "Failed to check network status. API error.")
                return None
        except Exception as e:
            self.show_popup("Error", f"Failed to check network status.\n{str(e)}")
            return None

    def check_network(self, instance):
        vpn_status = self.is_vpn()
        if vpn_status is None:
            return
        if vpn_status:
            self.show_popup("Network Status", "MTN Network is blocked for VPN users.")
        else:
            self.show_popup("Network Status", "Network access allowed. No VPN detected.")

    def show_popup(self, title, message):
        popup_content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        popup_label = Label(text=message)
        popup_button = Button(text="OK", size_hint=(1, 0.3))
        popup_content.add_widget(popup_label)
        popup_content.add_widget(popup_button)

        popup = Popup(title=title, content=popup_content, size_hint=(0.8, 0.4))
        popup_button.bind(on_press=popup.dismiss)
        popup.open()

class MTNNetworkBlockerApp(App):
    def build(self):
        return MTNNetworkBlockerMobile()

if __name__ == '__main__':
    MTNNetworkBlockerApp().run()
