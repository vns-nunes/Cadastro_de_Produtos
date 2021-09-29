from PyQt5 import uic,QtWidgets
import mysql.connector
from reportlab.pdfgen import canvas

numero_id = 0

#Acessando o servidor do banco de dados MySQL
banco = mysql.connector.connect(
    host='localhost',
    user='root',
    passwd='',
    database='cadastro_produtos'
)


def editar_dados():
    global numero_id

    linha = segunda_tela.tableWidget.currentRow()

    cursor = banco.cursor()
    cursor.execute("SELECT id FROM produtos")
    dados_lidos = cursor.fetchall()
    valor_id = dados_lidos[linha][0]
    cursor.execute("SELECT * FROM produtos WHERE id=" + str(valor_id))
    produto = cursor.fetchall()
    tela_editar.show()

    tela_editar.lineEdit.setText(str(produto[0][0]))
    tela_editar.lineEdit_2.setText(str(produto[0][1]))
    tela_editar.lineEdit_3.setText(str(produto[0][2]))
    tela_editar.lineEdit_4.setText(str(produto[0][3]))
    tela_editar.lineEdit_5.setText(str(produto[0][4]))
    numero_id = valor_id


def salvar_valor_editado():
    global numero_id

    # ler dados do lineEdit
    codigo = tela_editar.lineEdit_2.text()
    descricao = tela_editar.lineEdit_3.text()
    preco = tela_editar.lineEdit_4.text()
    categoria = tela_editar.lineEdit_5.text()
    # atualizar os dados no banco
    cursor = banco.cursor()
    cursor.execute(
        "UPDATE produtos SET codigo = '{}', descricao = '{}', preco = '{}', categoria ='{}' WHERE id = {}".format(
            codigo, descricao, preco, categoria, numero_id))
    banco.commit()
    # atualizar as janelas
    tela_editar.close()
    segunda_tela.close()
    chama_segunda_tela()


def excluir_dados():
    linha = segunda_tela.tableWidget.currentRow()
    segunda_tela.tableWidget.removeRow(linha)

    cursor = banco.cursor()
    cursor.execute('SELECT id FROM produtos')
    dados_lidos = cursor.fetchall()
    valor_id = dados_lidos[linha][0]
    cursor.execute('DELETE from produtos WHERE id='+ str(valor_id))





def gerar_pdf():
    print('gerar pdf')
    cursor = banco.cursor()
    comando_SQL = 'SELECT * FROM produtos'
    cursor.execute(comando_SQL)
    dados_lidos = cursor.fetchall()
    y = 0
    pdf = canvas.Canvas("cadastro_produtos.pdf")
    pdf.setFont("Times-Bold", 25)
    pdf.drawString(200, 800, "Produtos cadastrados:")
    pdf.setFont("Times-Bold", 18)

    pdf.drawString(10, 750, "ID")
    pdf.drawString(110, 750, "CODIGO")
    pdf.drawString(210, 750, "PRODUTO")
    pdf.drawString(310, 750, "PREÇO")
    pdf.drawString(410, 750, "CATEGORIA")

    for i in range(0, len(dados_lidos)):
        y = y + 50
        pdf.drawString(10, 750 - y, str(dados_lidos[i][0]))
        pdf.drawString(110, 750 - y, str(dados_lidos[i][1]))
        pdf.drawString(210, 750 - y, str(dados_lidos[i][2]))
        pdf.drawString(310, 750 - y, str(dados_lidos[i][3]))
        pdf.drawString(410, 750 - y, str(dados_lidos[i][4]))

    pdf.save()
    print("PDF FOI GERADO COM SUCESSO!")


#Criando a funçao principal e declarando as variáveis de acordo com os campos do formulário
def funcao_principal():
    linha1= projeto.lineEdit.text()
    linha2 = projeto.lineEdit_2.text()
    linha3 = projeto.lineEdit_3.text()
    categoria = ''

#Verificando qual radioButton foi selecionado e atribuindo na variável categoria
    if projeto.radioButton.isChecked():
        print('Categoria informática foi selecionado')
        categoria = 'Informática'
    elif projeto.radioButton_2.isChecked():
        print('Categoria Alimentos foi selecionado')
        categoria = 'Alimentos'
    elif projeto.radioButton_3.isChecked():
        print('Categoria Eletronicos foi selecionado')
        categoria = 'Eletronicos'

#Imprimindo as variáveis - apenas para verificação
    print('Codigo',linha1)
    print('Descrição', linha2)
    print('Preço', linha3)

#Conectando e manipulando o banco de dados - Inserindo linhas através do formulário
    cursor = banco.cursor()
    comando_SQL = 'INSERT INTO produtos(codigo,descricao,preco,categoria) VALUES (%s,%s,%s,%s)'
    dados = (str(linha1),str(linha2),str(linha3),categoria)
    cursor.execute(comando_SQL,dados)
    banco.commit()
#Limpando os campos após o envio
    projeto.lineEdit.setText('')
    projeto.lineEdit_2.setText('')
    projeto.lineEdit_3.setText('')

def chama_segunda_tela():
    segunda_tela.show()

    cursor = banco.cursor()
    comando_SQL = 'SELECT * FROM produtos'
    cursor.execute(comando_SQL)
    dados_lidos = cursor.fetchall()

    segunda_tela.tableWidget.setRowCount(len(dados_lidos))
    segunda_tela.tableWidget.setColumnCount(5)

    for i in range(0, len(dados_lidos)):
        for j in range(0,5):
            segunda_tela.tableWidget.setItem(i,j,QtWidgets.QTableWidgetItem(str(dados_lidos[i][j])))




app=QtWidgets.QApplication([])
projeto=uic.loadUi('projeto.ui')
segunda_tela=uic.loadUi('projeto9.ui')
tela_editar=uic.loadUi('projeto5.ui')
projeto.pushButton.clicked.connect(funcao_principal)
projeto.pushButton_2.clicked.connect(chama_segunda_tela)
segunda_tela.pushButton.clicked.connect(gerar_pdf)
segunda_tela.pushButton_2.clicked.connect(excluir_dados)
segunda_tela.pushButton_3.clicked.connect(editar_dados)
tela_editar.pushButton.clicked.connect(salvar_valor_editado)

projeto.show()


app.exec()

#Os comandos abaixo foram inseridos no terminal do mysql:
#Criando a tabela
# create table produtos (
#id INT NOT NULL AUTO_INCREMENT,
#codigo INT,
#descricao VARCHAR(50),
#preco DOUBLE,
#categoria VARCHAR (20),
#PRIMARY KEY (id)
#
# );

#Inserindo registros na tabela:

# INSERT INTO produtos (codigo, descricao, preco, categoria) VALUES (123,'Impressora',500.00,'informatica');

