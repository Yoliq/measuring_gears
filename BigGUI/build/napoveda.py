from tkinter import StringVar

class Napoveda:
    def __init__(self, napoveda_var: StringVar):
        self.messages = [
            "Nasaď správný vzorek",
            "Zadej název, datum a vyber složku",
            "Nastav osovou vzdálenost",
            "Utáhni svařenec páky ke stolu",
            "Zahoumuj",
            "Nastav začátek záběru",
            "Vynuluj snímače natočení",
            "Nasaď závaží",
            "Zapiš hmotnost závaží",
            "Prověď sekvenci měření",
            "Zkontroluj cestu a ulož",
            "Můžeš opakovat sekvenci dolů"
        ]
        self.current_message_index = 0
        self.napoveda_var = napoveda_var
        self.napoveda_var.set(self.messages[self.current_message_index])

    def dalsi_zprava(self):
        self.current_message_index = (self.current_message_index + 1) % len(self.messages)
        self.napoveda_var.set(self.messages[self.current_message_index])