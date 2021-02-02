from selenium import webdriver
import unittest
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
from django.test import LiveServerTestCase
import time

MAX_WAIT = 10

class NewVisitorTest(LiveServerTestCase):

    def setUp(self) -> None:
        self.browser = webdriver.Firefox()

    def tearDown(self) -> None:
        self.browser.quit()

    def wait_for_row_in_list_table(self, row_text):
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element_by_id('id_list_table')
                rows = table.find_elements_by_tag_name('tr')
                self.assertIn(row_text, [row.text for row in rows])
                return
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)

    def test_can_start_a_list_for_one_user(self):
        #Edith ouviu falar de uma nova aplicação online interessante para lista de tarefas. Ela decide verificar sua homepage
        self.browser.get(self.live_server_url)

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

        text_to_check = '1: Buy peacock feathers'
        self.wait_for_row_in_list_table(row_text=text_to_check)

        #ainda continua havendo uma caixa de texto convidando-a a acrrescentar outros
        #item. Ela insere "Use peackock feathers to make a fly" (usar penas de pavãos para dazer um fly - Edith é bem metódica)
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Use peacock feather to make a fly')
        inputbox.send_keys(Keys.ENTER)


        #A página é atualizada e agora mostra dois itens em sua lista
        text_to_check = '2: Use peacock feather to make a fly'
        self.wait_for_row_in_list_table(row_text=text_to_check)
        text_to_check = '1: Buy peacock feathers'
        self.wait_for_row_in_list_table(row_text=text_to_check)
        self.fail('test finish!')

        #edith se pergunta se o site lembrará de sua lista. Então ela nota que o site gerou um url unico para ele -- há um
        #pequenotexto explicativvo para isso

        #ela acessa a URL - dsua lista de tarefas continua lá

        # Satisfeita, ela volta a dormir.


    def test_multiple_users_can_start_lists_at_different_urls(self):
        #Edith inicia uma nova lista de tarefas
        self.browser.get(self.live_server_url)
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy peacock feathers')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table(row_text='1: Buy peacock feathers')

        #ela percebe que sua lista tem um URL unico
        edith_list_url = self.browser.current_url
        self.assertRegex(edith_list_url, '/lists/.+')

        #agora um novo usuário, francis, chega ao site

        #usamos uma nova sessão de navegador para garantir que nenhuma infomação de edith está vindo de cookies e etc
        self.browser.quit()
        self.browser = webdriver.Firefox()

        #francis acessa a pagina inicial. Não há nenhum sinal da lista de Edith
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertNotIn('make a fly', page_text)

        #francis inicia uma nova lista inserindo um item novo. ele
        #é menos interessante que Edith
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy milk')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy milk')

        #francis obtem seu proprio URL exclusivo
        francis_lis_url = self.browser.current_url
        self.assertRegex(francis_lis_url, '/lists/.+')
        self.assertNotEqual(francis_lis_url, edith_list_url)

        #novamente, não há nenhum sinal da lista de edith
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertIn('Buy milk', page_text)

        #satisfeito, ambos voltam a dormir
