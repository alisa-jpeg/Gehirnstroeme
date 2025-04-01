def forward(self):
  self.frame1.destroy()
  self.frame2.tkraise()


def createText(self):
#.cget("value") gibt den wert des eingabefeldes zurück
  v0 = radio_var0.get()
  kaffee = ""
        if v0 == 1:
            kaffee = "Innerhalb der letzten zwei Stunden"
        elif v0 == 2:
            kaffee = "Innerhalb der letzten 12 Stunden"
        elif v0  == 3:
            kaffee = "Vor über 12 Stunden"
        elif v0 == 4:
            kaffee = "Ich trinke keinen Kaffee"
        else:
            kaffee = "Keine Angabe"
  #text-variable füllen
        text = {"Alter": self.nameEntry.get(),
                "Kaffee getrunken": kaffee, 
                }
  return text

def validate_inputs(self):

        v0 = radio_var0.get()
        try:
            alter = int(self.nameEntry.get())
            if alter < 1 or alter > 120:
                raise ValueError
        except ValueError:
            msgbox.showerror("Fehler", "Bitte geben Sie ein gültiges Alter zwischen 1 und 120 ein.")
            return False

        if v0 == 0:
            msgbox.showerror("Fehler", "Bitte wählen Sie eine Option für den Kaffeekonsum.")
            return False
  return True

def endframe(self):
        if not self.validate_inputs():
            return
        self.filename = "versuchsdaten.csv"
        self.data = self.createText()
        msgbox.showinfo("Erfolg", "Die Daten wurden erfolgreich gespeichert.")
        self.forward()

def show_only(self):
        self.show_only_flag = True
        msgbox.showinfo("Nur zur Ansicht", "Keine Daten werden gespeichert. Dies dient nur der Anschauung.")
        self.show_only_flag = False
        self.forward()

def threading_average_alpha(self):
        self.startGameButton.configure(state = "disabled")        
        self.displayBox3.delete("0.0", "end")
        self.displayBox3.insert("0.0", "UDP-Stream läuft - Bitte warten Sie einen Moment")
        threading.Thread(target=self.show_alpha).start()

def show_alpha(self):
        self.alpha_average = calculate_average_alpha()
        self.displayBox1.delete("0.0", "end")
        self.displayBox1.insert("0.0", self.alpha_average)
        self.displayBox3.delete("0.0", "end")
        self.displayBox3.insert("0.0", "UDP-Stream ist abgeschlossen - Das Spiel kann beginnen!")
        self.startGameButton.configure(state = "normal")


def spiel_beginnen(self):
        self.label = ctk.CTkLabel(self.frame2, text="3...")
        self.label.grid(row=7, column=0, columnspan=2, padx=20, pady=20, sticky="w")
        self.after(1000, self.update_label, "2...")
    
def update_label(self, text):
  self.label.configure(text=text)
    if text == "2...":
        self.after(1000, self.update_label, "1...")
    elif text == "1...":
        self.after(1000, self.update_label, "Los!")
    elif text == "Los!":
        self.after(1000, self.start_game)

def start_game(self):
        success = self.move_ballon()
        text = success
        self.label.configure(text="")

        self.data["Erfolg"] = success
        safe_data(self.filename, self.data)




