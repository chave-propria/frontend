from js import document
from pyscript import when

class PopUp:
    def __init__(self, pop_up_id: str) -> None:
        self.popup = document.getElementById(pop_up_id)


    def show_popup(self, message: str) -> None:
        popup_message = document.getElementById("popupMessage")
        popup_message.innerText = str(message)
        self.popup.style.display = "block"

    @when('click', '#close')
    def close_popup(self) -> None:
        popup = document.getElementById("myPopup")
        popup.style.display = "none"


pop_up = PopUp(pop_up_id="myPopup")
