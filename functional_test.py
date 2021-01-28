from selenium import webdriver
import unittest

class NewVisitorTest(unittest.TestCase):

    def setUp(self) -> None:
        self.browser = webdriver.Firefox()

    def tearDown(self) -> None:
        self.browser.quit()

    def test_can_start_alist_and_retrieve_it_later(self):



        #Edith ouviu falar de uma nova aplicação online interessante para lista de tarefas. Ela decide verificar sua homepage
        self.browser.get('http://localhost:8000')

        #ela percebe que o titulo da pagina e o cabeçalho mencionam listas de tarefa (to-do)
        self.assertIn('To-Do lists', self.browser.title)
        self.fail('finish the test!')

        #ela é convidada a inserir um item de tarefa imediatamente

        #ela digita "buy peacock feathers" (Comprar penas de pavão) em uma caixa de texto
        #(o hobby de edith é fazer iscas para pescas com fly)

        #quando ela tecla enter, a página é atualizada e agora a página listas
        #1="1: buy peacock feathers" como um item em uma lista de tarefas

        #ainda continua havendo uma caixa de texto convidando-a a acrrescentar outros
        #item. Ela insere "Use peackock feathers to make a fly" (usar penas de pavãos para dazer um fly - Edith é bem metódica)

        #A página é atualizada e agora mostra dois itens em sua lista

        #edith se pergunta se o site lembrará de sua lista. Então ela nota que o site gerou um url unico para ele -- há um
        #pequenotexto explicativvo para isso

        #ela acessa a URL - dsua lista de tarefas continua lá

        # Satisfeita, ela volta a dormir.

if __name__ == '__main__':
    unittest.main(warnings='ignore')
