from selenium import webdriver
import unittest
from selenium.webdriver.common.keys import Keys
import time


class NewVisitorTest(unittest.TestCase):

    def setUp(self) -> None:
        self.browser = webdriver.Firefox()

    def tearDown(self) -> None:
        self.browser.quit()

    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

    def test_can_start_alist_and_retrieve_it_later(self):
        #Edith ouviu falar de uma nova aplicação online interessante para lista de tarefas. Ela decide verificar sua homepage
        self.browser.get('http://localhost:8000')

        #ela percebe que o titulo da pagina e o cabeçalho mencionam listas de tarefa (to-do)
        self.assertIn('To-Do lists', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertEqual(
            'Your To-Do list', header_text
        )

        #ela é convidada a inserir um item de tarefa imediatamente
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item'
        )

        #ela digita "buy peacock feathers" (Comprar penas de pavão) em uma caixa de texto
        #(o hobby de edith é fazer iscas para pescas com fly)
        inputbox.send_keys('Buy peacock feathers')

        #quando ela tecla enter, a página é atualizada e agora a página listas
        #1="1: buy peacock feathers" como um item em uma lista de tarefas
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        text_to_check = '1: Buy peacock feathers'
        self.check_for_row_in_list_table(row_text=text_to_check)

        #ainda continua havendo uma caixa de texto convidando-a a acrrescentar outros
        #item. Ela insere "Use peackock feathers to make a fly" (usar penas de pavãos para dazer um fly - Edith é bem metódica)
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Use peacock feather to ake a fly')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)


        #A página é atualizada e agora mostra dois itens em sua lista
        text_to_check = '2: Use peacock feather to make a fly'
        self.check_for_row_in_list_table(row_text=text_to_check)
        text_to_check = '1: Buy peacock feathers'
        self.check_for_row_in_list_table(row_text=text_to_check)
        self.fail('test finish!')

        #edith se pergunta se o site lembrará de sua lista. Então ela nota que o site gerou um url unico para ele -- há um
        #pequenotexto explicativvo para isso

        #ela acessa a URL - dsua lista de tarefas continua lá

        # Satisfeita, ela volta a dormir.

if __name__ == '__main__':
    unittest.main(warnings='ignore')
