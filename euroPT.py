# -*- coding: utf-8 -*-
from kivy.app import App
from kivy.properties import StringProperty
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.network.urlrequest import UrlRequest
from settingsjson import settings_json

__version__ = '0.5.0'

Builder.load_string('''
<staButton@Button>:
    text_size: self.width, None
    halign: 'center'
    size_hint_x: 0.2
    background_color: (0.4, 0.4, 0.4, 1.0)
    padding_x: 4
<queryTOData>:
    GridLayout:
        cols: 2
        Button:
            text: "Settings"
            on_release: app.open_settings()
            background_color: (0.4, 0.4, 0.4, 1.0)
            size_hint_x: 0.25
            size_hint_y: 0.4
        Label:
            text: "EU/CH stationboards"
            text_size: self.width, None
            halign: 'center'
            color: .8,.9,0,1
            size_hint_y: 0.4
        staButton:
            text: "update: " + root.stA
            on_release: root.lookup(root.stA)
        Label:
            text: root.foundA
            text_size: self.width, None
            padding_x: 10
        staButton:
            text: "update: " + root.stB
            on_release: root.lookup(root.stB)
        Label:
            text: root.foundB
            text_size: self.width, None
            padding_x: 10
        staButton:
            text: "update: " + root.stC
            on_release: root.lookup(root.stC)
        Label:
            text: root.foundC
            text_size: self.width, None
            padding_x: 10
        staButton:
            text: "update: " + root.stD
            on_release: root.lookup(root.stD)
        Label:
            text: root.foundD
            text_size: self.width, None
            padding_x: 10
''')

limit = "&limit=6"
urlStation = "http://transport.opendata.ch/v1/stationboard?station="


class queryTOData(Screen):
    stA = StringProperty("")
    stB = StringProperty("")
    stC = StringProperty("")
    stD = StringProperty("")
    foundA = StringProperty("")
    foundB = StringProperty("")
    foundC = StringProperty("")
    foundD = StringProperty("")

    def __init__(self, **kwargs):
        super(queryTOData, self).__init__(**kwargs)
        self.stA = "Basel, Schuetzenhaus"
        self.stB = "Erasmusplatz"
        self.stC = "Johanniterbruecke"
        self.stD = "Brausebad"
        self.foundA = ""
        self.foundB = ""
        self.foundC = ""
        self.foundD = ""
        #print(kivyTOData.config.get("stations", "station1"))

    def req(*args):
        r = UrlRequest(urlStation + args[1] + limit)
        r.wait()
        jData = r.result
        stb = jData.get("stationboard")
        accuStr = []

        for i in range(len(stb)):
            tName = stb[i].get("name")
            tDest = stb[i].get("to")
            tDepTime = stb[i].get("stop").get("departure")
            displayStr = tName + ", "
            displayStr += tDepTime[11:16] + ", "
            displayStr += tDest
            if i < 7:
                accuStr += "\n" + displayStr
        return accuStr

    def lookup(self, *args):
        print(args[0])
        if args[0] == self.stA:
            self.foundA = ""
            for line in self.req(args[0]):
                self.foundA += line
        elif args[0] == self.stB:
            self.foundB = ""
            for line in self.req(args[0]):
                self.foundB += line
        elif args[0] == self.stC:
            self.foundC = ""
            for line in self.req(args[0]):
                self.foundC += line
        elif args[0] == self.stD:
            self.foundD = ""
            for line in self.req(args[0]):
                self.foundD += line


sm = ScreenManager()
sm.add_widget(queryTOData(name="queryTOData"))


class kivyTOData(App):

    def build(self):
        self.use_kivy_settings = False
        #settings = self.config.items("stations")
        #print(self.config.get("stations", "station1"))
        sm.children[0].stA = self.config.get("stations", "station1")
        sm.children[0].stB = self.config.get("stations", "station2")
        sm.children[0].stC = self.config.get("stations", "station3")
        sm.children[0].stD = self.config.get("stations", "station4")
        return sm

    def build_config(self, config):
        config.setdefaults("stations", {"station1": "Voltaplatz",
                                        "station2": "Erasmusplatz",
                                        "station3": "Johanniterbruecke",
                                        "station4": "Freilager"})

    def build_settings(self, settings):
        settings.add_json_panel("set-up", self.config, data=settings_json)

    def on_config_change(self, config, section, key, value):
        if key == "station1":
            sm.children[0].stA = value
        elif key == "station2":
            sm.children[0].stB = value
        elif key == "station3":
            sm.children[0].stC = value
        elif key == "station4":
            sm.children[0].stD = value
        print config, section, key, value

    def on_pause(self):
        return True

    def on_resume(self):
        pass


if __name__ == "__main__":
    kivyTOData().run()