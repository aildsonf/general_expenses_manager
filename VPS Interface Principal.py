from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
import SaldoDataBase
import DespesasData
import DespesaSomaBD
from GraficoTotalDespesas import GetGrafico, GetGraficoPeriodo
from tkcalendar import *
from tkinter import messagebox
import datetime

class Controlador:
    def GetSaldo(self):
        self.saldo_Atual = 00.00
        SaldoDataBase.cursor.execute("""
                                                  SELECT * FROM SaldoData WHERE (ID = 1)
                                                  """)
        self.saldo_Atual2 = SaldoDataBase.cursor.fetchone()
        if self.saldo_Atual2 == None:
            SaldoDataBase.cursor.execute("""
                                                      INSERT INTO SaldoData(VALOR) VALUES(?)
                                                     """, (self.saldo_Atual,))
            SaldoDataBase.conn.commit()
            return self.saldo_Atual
        else:
            self.saldo_Atual = self.saldo_Atual2
            self.valor_Saldo = self.saldo_Atual[1]
            self.Despesas = self.GetValorDespesas()
            self.valor_final = self.valor_Saldo - self.Despesas
            return self.valor_final

    def GetSaldoInicial(self):
        self.saldo_Atual = 00.00
        SaldoDataBase.cursor.execute("""
                                                          SELECT * FROM SaldoData WHERE (ID = 1)
                                                          """)
        self.saldo_Atual2 = SaldoDataBase.cursor.fetchone()
        if self.saldo_Atual2 == None:
            SaldoDataBase.cursor.execute("""
                                                              INSERT INTO SaldoData(VALOR) VALUES(?)
                                                             """, (self.saldo_Atual,))
            SaldoDataBase.conn.commit()
            return self.saldo_Atual
        else:
            self.saldo_Atual = self.saldo_Atual2
            self.valor_Saldo = self.saldo_Atual[1]
            return self.valor_Saldo

    def GetValorDespesas(self):
        self.somador = 00.00
        DespesasData.cursor.execute("""
                                      SELECT VALOR FROM Despesas
                                      """)
        self.despesas_Atual2 = DespesasData.cursor.fetchall()
        print(self.despesas_Atual2)
        if self.despesas_Atual2 == None:
            self.somador = 00.00
        else:
            for x in range(len(self.despesas_Atual2)):
                self.somador = self.despesas_Atual2[x][0] + self.somador
            print(self.somador)
        return self.somador

    def InserirSaldo(self,saldo):
        try:
            saldoFloat = float(saldo)
            print(saldoFloat)
            if saldoFloat < 0:
                messagebox.showerror(title='Error na Operção', message="Valor não Aceito")
            else:
                SaldoDataBase.cursor.execute("""
                          UPDATE SaldoData SET VALOR = ? WHERE ID = ?
                         """,(saldoFloat,1))
                SaldoDataBase.conn.commit()
                messagebox.showinfo(title='Register log', message="Saldo Adicionado com Sucesso")
        except:
            messagebox.showerror(title='Error na Operção', message="Valor não Aceito")

    def RegistrarDespesa(self,nome,quantidade,valor,calendario):
        try:
            self.nome1 = nome.lower()
            self.quantidade1 = quantidade
            self.valor1 = valor
            self.calendario1 = calendario
            DespesasData.cursor.execute("""
                           SELECT * FROM Despesas WHERE (NOME = ? and CALENDARIO = ?)
                           """, (self.nome1, self.calendario1))
            self.verify = DespesasData.cursor.fetchone()
            print(self.verify)
            if self.nome1 == '' or self.quantidade1 == '' or self.calendario1 == '' or self.valor1 == '':
                messagebox.showwarning(title='Register Error', message="Preencha todos os campos")
            elif self.verify != None:
                if self.nome1 in self.verify and self.calendario1 in self.verify:
                    messagebox.showerror(title='Register Error', message="Despesa já adicionada")
            elif self.nome1 != '' and self.quantidade1 != '' and self.calendario1 != '' and self.valor1 != '':
                self.valortest = float(self.valor1)
                self.quantidade1 = int(self.quantidade1)
                if self.quantidade1 > 0 and self.valortest >= 0:
                    self.valor2 = float(self.valor1)
                    self.quantidade2 = str(self.quantidade1)
                    DespesasData.cursor.execute("""
                          INSERT INTO Despesas(NOME,QUANTIDADE,VALOR,CALENDARIO) VALUES(?,?,?,?)
                                                                                              """,
                                                (self.nome1, self.quantidade2, self.valor2, self.calendario1))
                    DespesasData.conn.commit()
                    messagebox.showinfo(title='Register log', message="Despesa Adicionado com Sucesso")
                    self.RegisterGraficoDataBase(self.calendario1,self.quantidade2,self.valor2)
                else:
                    messagebox.showerror(title='Register Error', message="Error na operação \n verifique as entradas")

        except:
            messagebox.showerror(title='Register Error', message="Error na operação \n verifique as entradas")

    def RemoverDespesa(self,nome,quantidade,valor,calendario):
        try:
            self.nome = nome.lower()
            self.quantidade = quantidade
            self.valor = valor
            self.calendario = calendario
            if self.nome == '' or self.quantidade == '' or self.calendario == '' or self.valor == '':
                messagebox.showwarning(title='Register Error', message="Preencha todos os campos")
            else:
                self.valor2 = float(self.valor)
                DespesasData.cursor.execute("""
                        SELECT * FROM Despesas WHERE (NOME = ? and CALENDARIO = ? and QUANTIDADE = ? and VALOR = ?)
                                                        """, (self.nome, self.calendario, self.quantidade, self.valor2))
                self.verify = DespesasData.cursor.fetchone()
                print(self.verify)
                if self.verify == None:
                    messagebox.showerror(title='Register Error', message="Nenhuma Despesa Encontrada")
                else:
                    valor2 = float(self.valor)
                    print(self.quantidade)
                    DespesasData.cursor.execute("""
                        DELETE FROM Despesas WHERE (NOME = ? and CALENDARIO = ? and VALOR = ?and QUANTIDADE = ?)
                                                            """,(self.nome, self.calendario, self.valor2, self.quantidade))
                    DespesasData.conn.commit()
                    messagebox.showinfo(title='Register log', message="Despesa Removida com Sucesso")
                    self.RemoverGraficoDataBase(self.calendario,self.quantidade,self.valor2)
        except:
            messagebox.showerror(title='Register Error', message="Valor não Aceito")

    def RegisterGraficoDataBase(self, calendario, quantidade, valor):
        self.calend = calendario
        self.quant = quantidade
        self.vall = valor
        DespesasData.cursor.execute("""
                                   SELECT CALENDARIO FROM Despesas WHERE (CALENDARIO = ?)
                                   """, (self.calend,))
        self.verifica = DespesasData.cursor.fetchone()
        if self.calend in self.verifica:
            DespesasData.cursor.execute("""
                                               SELECT VALOR, QUANTIDADE FROM Despesas WHERE (CALENDARIO = ?)
                                               """, (self.calend,))
            self.valoriza = DespesasData.cursor.fetchall()
            print(f'somador funcionando   {self.valoriza}')
            self.somadorValores = 00.00
            self.somadorQuantidade = 0
            for x in range(len(self.valoriza)):
                self.somadorValores = self.somadorValores + self.valoriza[x][0]
                self.somadorQuantidade = self.somadorQuantidade + int(self.valoriza[x][1])
            print(self.somadorValores)
            print(self.somadorQuantidade)
            DespesaSomaBD.cursor.execute("""
                                   SELECT CALENDARIO FROM DespesasSoma WHERE (CALENDARIO = ?)
                                   """, (self.calend,))
            self.verifi = DespesaSomaBD.cursor.fetchone()
            if self.verifi != None:
                if self.calend in self.verifi:
                    DespesaSomaBD.cursor.execute("""
                                        UPDATE DespesasSoma SET QUANTIDADE = ?, VALOR = ? WHERE (CALENDARIO = ?)
                                                       """, (self.somadorQuantidade, self.somadorValores, self.calend))
                    DespesaSomaBD.conn.commit()
            else:
                DespesaSomaBD.cursor.execute("""
                                          INSERT INTO DespesasSoma(QUANTIDADE,VALOR,CALENDARIO) VALUES(?,?,?)
                                          """, (self.somadorQuantidade, self.somadorValores, self.calend))
                DespesaSomaBD.conn.commit()
    def RemoverGraficoDataBase(self, calendario, quantidade, valor):
        self.calend = calendario
        self.quant = quantidade
        self.vall = valor
        DespesaSomaBD.cursor.execute("""
                                   SELECT CALENDARIO FROM DespesasSoma WHERE (CALENDARIO = ?)
                                   """, (self.calend,))
        self.verifica = DespesaSomaBD.cursor.fetchone()
        if self.verifica != None:
            if self.calend in self.verifica:
                DespesaSomaBD.cursor.execute("""
                                            SELECT VALOR, QUANTIDADE FROM DespesasSoma WHERE (CALENDARIO = ?)
                                                              """, (self.calend,))
                self.valoriza = DespesaSomaBD.cursor.fetchall()
                self.quantidadeSomador = self.valoriza[0][1]
                self.valorSomador = self.valoriza[0][0]
                self.valorSomadorNovo = self.valorSomador - float(self.vall)
                self.quantidadeSomadorNovo = self.quantidadeSomador - int(self.quant)
                DespesaSomaBD.cursor.execute("""
                                        UPDATE DespesasSoma SET QUANTIDADE = ?, VALOR = ?  WHERE CALENDARIO = ?
                                                                       """,
                                             (self.quantidadeSomadorNovo, self.valorSomadorNovo, self.calend))
                DespesaSomaBD.conn.commit()

class JanelaPrincipal:
    def Iniciar(self):
        self.Janela()
        self.Widgets()
        self.Bottons()
        self.jan.mainloop()
    def Janela(self):
        self.jan = Tk()
        self.jan.title('VPSBank---By Niciu feat Panini------')
        self.jan.geometry('390x350')
        self.jan.configure(background='white')
        self.jan.resizable(width=False, height=False)
    def Widgets(self):
        self.canvas = Canvas(self.jan, width=600, height=400, bg='MIDNIGHTBLUE', relief='raise')
        self.wallpaper = ImageTk.PhotoImage(Image.open('Wallpapers/imagem7.gif'))
        self.canvas.create_image(0, 0, anchor=NW, image=self.wallpaper)
        self.canvas.create_text(300, 70, fill="black", font="Times 16 italic bold",
                           text="Saldo Atual:")
        self.canvas.create_text(100, 70, fill="black", font="Times 16 italic bold",
                           text="Despesas Totais:")
        self.canvas.pack(side=LEFT)
    def Bottons(self):
        self.config_Saldo = ttk.Button(self.canvas, text='   Configurações   \n         de    \n       Saldo     ', width=24
                                  ,command=lambda: JanelaConfigSaldo().Iniciar())
        self.config_Saldo.place(x=20, y=190)

        self.config_Despesa = ttk.Button(self.canvas, text='Configurações\n       de\n   Despesas', width=24,
                                    command=lambda: JanelaConfDespesas().Iniciar())
        self.config_Despesa.place(x=20, y=270)

        self.visualizador = ttk.Button(self.canvas, text='  Vizualizador     \n        de  \n    Despesas      ', width=24
                                  ,command=lambda: JanelaDespesas().Iniciar())
        self.visualizador.place(x=220, y=190)

        AtualizarSaldo = ttk.Button(self.canvas, text='  Atualizar ', width=14,
                                    command=lambda:[self.saldoLabel.config(text=f'R${Controlador().GetSaldo()}'),
                                        self.depesasLabel.config(text=f'R${Controlador().GetValorDespesas()}')])
        AtualizarSaldo.place(x=280, y=9)

        self.planejador = ttk.Button(self.canvas, text='            Informações \n                     e\n       Créditos do Criador      ', width=24,
                                     command=lambda: messagebox.showinfo(title='App Info', message="\nApp Versão Beta I\nApp Criado em parceria\n ---Niciu e Panini----\n"
                                                                                                   "Todas as imagens são de autoria de:"
                                                                                                   "\n---Rebecca Mock----\n Por favor, Apoie a Artista"
                                                                                                   "\n App Criado Sem Fiz Lucrativos"
                                                                                                   "\n App Desenvolvido para Estudos \n"))
        self.planejador.place(x=220, y=270)

        self.saldoLabel = Label(self.canvas, text=f'R${Controlador().GetSaldo()}', font=('Century Gthic', 14), bg='black', fg='white')
        self.saldoLabel.place(x=240, y=90)

        self.depesasLabel = Label(self.canvas, text=f'R${Controlador().GetValorDespesas()}', font=('Century Gthic', 14), bg='black',
                             fg='white')
        self.depesasLabel.place(x=80, y=90)

class JanelaConfigSaldo:
    def Iniciar(self):
        self.janela()
        self.Widgets()
        self.Bottons()
        self.jan2.mainloop()

    def janela(self):
        self.jan2 = Toplevel()
        self.jan2.title('VPSBank---Configurações de Saldo')
        self.jan2.geometry('390x250')
        self.jan2.configure(background='white')
        self.jan2.resizable(width=False, height=False)
    def Widgets(self):
        self.canvas = Canvas(self.jan2, width=600, height=400, bg='MIDNIGHTBLUE', relief='raise')
        self.wallpaper2 = ImageTk.PhotoImage(Image.open('Wallpapers/saldo.gif'))
        self.canvas.create_image(0, 0, anchor=NW, image=self.wallpaper2)
        self.canvas.create_text(200, 70, fill="BLACK", font="Times 20 italic bold",
                           text="Saldo Inicial:")
        self.canvas.pack(side=LEFT)
    def Bottons(self):
        self.saldoEntry = ttk.Entry(self.canvas, width=25)
        self.saldoEntry.place(x=120, y=190)
        self.inserir_Saldo = ttk.Button(self.canvas, text='Inserir Saldo', width=14,
                                        command= lambda:[Controlador().InserirSaldo(self.saldoEntry.get()),
                                        self.saldoAtualLabel.config(text=f'R${Controlador().GetSaldoInicial()}')])
        self.inserir_Saldo.place(x=20, y=190)
        self.saldoAtualLabel = Label(self.canvas, text=f'R${Controlador().GetSaldoInicial()}',
                                    font=('Century Gthic', 17), bg='BLACK', fg='WHITE')
        self.saldoAtualLabel.place(x=100, y=90)

class JanelaConfDespesas:
    def Iniciar(self):
        self.Janela()
        self.Widgets()
        self.Bottons()
        self.jan3.mainloop()

    def Janela(self):
        self.jan3 = Toplevel()
        self.jan3.title('VPSBank---Configurações de Despesas')
        self.jan3.geometry('380x400')
        self.jan3.configure(background='white')
        self.jan3.resizable(width=False, height=False)

    def Widgets(self):
        self.canvas = Canvas(self.jan3, width=600, height=400, bg='MIDNIGHTBLUE', relief='raise')
        self.wallpaper2 = ImageTk.PhotoImage(Image.open('Wallpapers/despesas.jpg'))
        self.canvas.create_image(0, 0, anchor=NW, image=self.wallpaper2)
        self.canvas.create_text(120, 50, fill="white", font="Times 18 italic bold",
                                text="Despesas Totais")
        self.canvas.create_text(140, 160, fill="white", font="Times 18 italic bold",
                                text="Informações da Despesa:")
        self.canvas.create_text(50, 190, fill="white", font="Times 18 italic bold",
                                text="Nome:")
        self.canvas.create_text(70, 220, fill="white", font="Times 18 italic bold",
                                text="Quantidade:")
        self.canvas.create_text(70, 250, fill="white", font="Times 18 italic bold",
                                text="Valor Total:")
        self.canvas.create_text(40, 280, fill="white", font="Times 18 italic bold",
                                text="Data:")
        self.canvas.pack(side=LEFT)

    def Bottons(self):
        self.nomeEntry = ttk.Entry(self.canvas, width=25)
        self.nomeEntry.place(x=100, y=180)
        self.QuantidadeEntry = ttk.Entry(self.canvas, width=25)
        self.QuantidadeEntry.place(x=140, y=210)
        self.ValorTotalEntry = ttk.Entry(self.canvas, width=25)
        self.ValorTotalEntry.place(x=140, y=240)
        current_time = datetime.datetime.now()
        self.cal = DateEntry(self.canvas, date_pattern='dd/mm/y', width=14, year=current_time.year,
                             month=current_time.month, day=current_time.day,
                             background='white',
                             foreground='black', borderwidth=25)
        self.cal.place(x=80, y=270)

        self.adicionar_Despesa = ttk.Button(self.canvas, text='Adicionar', width=24,
        command=lambda:[Controlador().RegistrarDespesa(self.nomeEntry.get(),self.QuantidadeEntry.get(),
                                                       self.ValorTotalEntry.get(),self.cal.get()),
                        self.despesasAtualLabel.config(text=f'R$ {Controlador().GetValorDespesas()}')])
        self.adicionar_Despesa.place(x=20, y=300)
        self.remover_Despesa = ttk.Button(self.canvas, text='Remover', width=24
                  ,command=lambda:[Controlador().RemoverDespesa(self.nomeEntry.get(),self.QuantidadeEntry.get(),
                            self.ValorTotalEntry.get(),self.cal.get()),
                            self.despesasAtualLabel.config(text=f'R$ {Controlador().GetValorDespesas()}'),])

        self.remover_Despesa.place(x=20, y=335)
        self.visualizarDespesa = ttk.Button(self.canvas, text='Visualizar \n Despesas', width=24
                                            ,command=lambda: JanelaDespesasVisualizador().TodasDespesas())
        self.visualizarDespesa.place(x=210, y=305)
        self.despesasAtualLabel = Label(self.canvas, text=f'R${Controlador().GetValorDespesas()}',
                                        font=('Century Gthic', 17), bg='BLACK',
                                        fg='WHITE')
        self.despesasAtualLabel.place(x=90, y=70)

class JanelaDespesas:
    def Iniciar(self):
        self.Janela()
        self.Widgets()
        self.Bottons()
        self.jan4.mainloop()
    def Janela(self):
        self.jan4 = Toplevel()
        self.jan4.title('VPSBank---Visualizador de Despesas')
        self.jan4.geometry('570x330')
        self.jan4.configure(background='white')
        self.jan4.resizable(width=False, height=False)
    def Widgets(self):
        self.canvas = Canvas(self.jan4, width=600, height=400, bg='MIDNIGHTBLUE', relief='raise')
        self.wallpaper2 = ImageTk.PhotoImage(Image.open('Wallpapers/visualizador.jpg'))
        self.canvas.create_image(0, 0, anchor=NW, image=self.wallpaper2)
        self.canvas.create_text(495, 220, fill="black", font="Times 18 italic bold",
                                text="Período:")
        self.canvas.create_text(410, 250, fill="black", font="Times 18 italic bold",
                           text="Início:")
        self.canvas.create_text(410, 290, fill="black", font="Times 18 italic bold",
                           text="Final:")
        self.canvas.create_text(280, 70, fill="black", font="Times 16 italic bold",
                           text="Saldo Atual:")
        self.canvas.create_text(450, 70, fill="black", font="Times 16 italic bold",
                           text="Saldo Inicial:")
        self.canvas.create_text(100, 70, fill="black", font="Times 16 italic bold",
                           text="Despesas Totais:")
        self.canvas.pack(side=LEFT)
    def Bottons(self):
        self.visualizarTodasDespesas = ttk.Button(self.canvas, text='Visualizar \n Todas \nDespesas', width=24,
                                             command=lambda: JanelaDespesasVisualizador().TodasDespesas())
        self.visualizarTodasDespesas.place(x=20, y=200)

        self.visualizarDataDespesas = ttk.Button(self.canvas, text='Visualizar Despesas \n            por \n        Período',
                                            width=24,command=lambda:
            JanelaDespesasPeriodo().PeriodoDespesas(self.cal1.get(),self.cal2.get()))
        self.visualizarDataDespesas.place(x=20, y=260)

        current_time = datetime.datetime.now()

        self.cal1 = DateEntry(self.canvas, date_pattern='dd/mm/y', width=14, year=current_time.year
                              , month=current_time.month, day=current_time.day, background='white',
                         foreground='black', borderwidth=25)
        self.cal1.place(x=445, y=241)

        self.cal2 = DateEntry(self.canvas, date_pattern='dd/mm/y', width=14, year=current_time.year
                              , month=current_time.month, day=current_time.day, background='white',
                         foreground='black', borderwidth=25)
        self.cal2.place(x=445, y=280)
        self.saldoLabel = Label(self.canvas, text=f'R${Controlador().GetSaldo()}', font=('Century Gthic', 14), bg='black', fg='white')
        self.saldoLabel.place(x=240, y=90)

        self.depesasLabel = Label(self.canvas, text=f'R${Controlador().GetValorDespesas()}', font=('Century Gthic', 14), bg='black',
                             fg='white')
        self.depesasLabel.place(x=80, y=90)

        self.saldoInicialLabel = Label(self.canvas, text=f'R${Controlador().GetSaldoInicial()}', font=('Century Gthic', 14), bg='black',
                                  fg='white')
        self.saldoInicialLabel.place(x=420, y=90)

        self.GraficoTodasDespesas = ttk.Button(self.canvas, text='Gráfico \n Todas \nDespesas', width=24,
                                               command= GetGrafico)
        self.GraficoTodasDespesas.place(x=180, y=200)
        self.GraficoPeridoDespesas = ttk.Button(self.canvas, text='Gráfico Despesas \n           por \n        Período', width=24,
                                                command=lambda: GetGraficoPeriodo(self.cal1.get(),self.cal2.get()))
        self.GraficoPeridoDespesas.place(x=180, y=260)

class JanelaDespesasVisualizador:
    def TodasDespesas(self):
        # ==================Janela=====================================================================================
        jan4 = Toplevel()
        jan4.title('VPSBank---Visualizador de Despesas')
        jan4.geometry('570x330')
        jan4.configure(background='white')
        jan4.resizable(width=False, height=False)
        # =================================Widgets=====================================================================
        canvas = Canvas(jan4, width=600, height=400, bg='MIDNIGHTBLUE', relief='raise')
        wallpaper2 = ImageTk.PhotoImage(Image.open('Wallpapers/visualizador.jpg'))
        canvas.create_image(0, 0, anchor=NW, image=wallpaper2)
        canvas.create_text(178, 19, fill="white", font="Times 12 italic bold",
                           text="Ordenar por:")
        lista = ttk.Treeview(canvas, height=3, column=('col1', 'col2', 'col3', 'col4', 'col5'))
        lista.column('#0', width=0)
        lista.heading('#1', text='ID')
        lista.heading('#2', text='NOME')
        lista.heading('#3', text='QUANTIDADE')
        lista.heading('#4', text='VALOR')
        lista.heading('#5', text='DATA')
        lista.heading('#0', text='')

        lista.column('#1', width=50)
        lista.column('#2', width=50)
        lista.column('#3', width=50)
        lista.column('#4', width=50)
        lista.column('#5', width=50)
        lista.place(relx=0.02, rely=0.1, relwidth=0.95, relheight=0.85)

        scroolLista = Scrollbar(canvas, orient='vertical')
        lista.configure(yscroll=scroolLista.set)
        scroolLista.place(relx=0.96, rely=0.1, relwidth=0.04, relheight=0.85)
        canvas.pack(side=LEFT)
        DespesasData.cursor.execute("""
        SELECT ID, NOME, QUANTIDADE, VALOR, CALENDARIO FROM Despesas ORDER BY ID
        """)
        despesas = DespesasData.cursor.fetchall()
        print(despesas)
        for i in despesas:
            lista.insert('', END, values=i)

        def Atualizar():
            lista.delete(*lista.get_children())
            DespesasData.cursor.execute("""
                        SELECT ID, NOME, QUANTIDADE, VALOR, CALENDARIO FROM Despesas ORDER BY ID
                        """)
            despesas = DespesasData.cursor.fetchall()
            print(despesas)
            for i in despesas:
                lista.insert('', END, values=i)

        def OrdenarNome():
            lista.delete(*lista.get_children())
            DespesasData.cursor.execute("""
                        SELECT ID, NOME, QUANTIDADE, VALOR, CALENDARIO FROM Despesas ORDER BY NOME
                        """)
            despesas = DespesasData.cursor.fetchall()
            print(despesas)
            for i in despesas:
                lista.insert('', END, values=i)

        def OrdenarQuantidade():
            lista.delete(*lista.get_children())
            DespesasData.cursor.execute("""
                        SELECT ID, NOME, QUANTIDADE, VALOR, CALENDARIO FROM Despesas ORDER BY QUANTIDADE
                        """)
            despesas = DespesasData.cursor.fetchall()
            print(despesas)
            for i in despesas:
                lista.insert('', END, values=i)

        def OrdenarValor():
            lista.delete(*lista.get_children())
            DespesasData.cursor.execute("""
                        SELECT ID, NOME, QUANTIDADE, VALOR, CALENDARIO FROM Despesas ORDER BY VALOR
                        """)
            despesas = DespesasData.cursor.fetchall()
            print(despesas)
            for i in despesas:
                lista.insert('', END, values=i)

        def OrdenarDATA():
            lista.delete(*lista.get_children())
            DespesasData.cursor.execute("""
                        SELECT ID, NOME, QUANTIDADE, VALOR, CALENDARIO FROM Despesas ORDER BY CALENDARIO
                        """)
            despesas = DespesasData.cursor.fetchall()
            print(despesas)
            for i in despesas:
                lista.insert('', END, values=i)

        Atualizar = ttk.Button(canvas, text='  Atualizar ', width=18, command=Atualizar)
        Atualizar.place(x=12, y=8)

        OrdenarNome = ttk.Button(canvas, text='Nome', width=12, command=OrdenarNome)
        OrdenarNome.place(x=224, y=8)

        OrdenarQuantidade = ttk.Button(canvas, text='Quantidade', width=12, command=OrdenarQuantidade)
        OrdenarQuantidade.place(x=305, y=8)

        OrdernarValor = ttk.Button(canvas, text='Valor', width=12, command=OrdenarValor)
        OrdernarValor.place(x=386, y=8)

        OrdernarDATA = ttk.Button(canvas, text='Data', width=12, command=OrdenarDATA)
        OrdernarDATA.place(x=467, y=8)

        jan4.mainloop()

class JanelaDespesasPeriodo:
    def PeriodoDespesas(self,inicio1,fim1):
        # ==================Janela=====================================================================================
        jan4 = Toplevel()
        jan4.title('VPSBank---Visualizador de Despesas por Periodo')
        jan4.geometry('570x330')
        jan4.configure(background='white')
        jan4.resizable(width=False, height=False)
        # =================================Widgets=====================================================================
        canvas = Canvas(jan4, width=600, height=400, bg='MIDNIGHTBLUE', relief='raise')
        wallpaper2 = ImageTk.PhotoImage(Image.open('Wallpapers/visualizador.jpg'))
        canvas.create_image(0, 0, anchor=NW, image=wallpaper2)
        canvas.create_text(178, 19, fill="white", font="Times 12 italic bold",
                           text="Ordenar por:")
        lista = ttk.Treeview(canvas, height=3, column=('col1', 'col2', 'col3', 'col4', 'col5'))
        lista.column('#0', width=0)
        lista.heading('#1', text='ID')
        lista.heading('#2', text='NOME')
        lista.heading('#3', text='QUANTIDADE')
        lista.heading('#4', text='VALOR')
        lista.heading('#5', text='DATA')
        lista.heading('#0', text='')

        lista.column('#1', width=50)
        lista.column('#2', width=50)
        lista.column('#3', width=50)
        lista.column('#4', width=50)
        lista.column('#5', width=50)
        lista.place(relx=0.02, rely=0.1, relwidth=0.95, relheight=0.85)

        scroolLista = Scrollbar(canvas, orient='vertical')
        lista.configure(yscroll=scroolLista.set)
        scroolLista.place(relx=0.96, rely=0.1, relwidth=0.04, relheight=0.85)
        canvas.pack(side=LEFT)
        DespesasData.cursor.execute("""
        SELECT ID, NOME, QUANTIDADE, VALOR, CALENDARIO FROM Despesas ORDER BY ID
        """)
        despesas = DespesasData.cursor.fetchall()
        inicio = int(inicio1.replace('/', ''))
        final = int(fim1.replace('/', ''))
        x = 0
        for i in despesas:
            z = int(despesas[x][4].replace('/', ''))
            x += 1
            if inicio <= z and z <= final:
                lista.insert('', END, values=i)
    # -------------------------- funções da janela ---------------------------------------------------------------------
        def Atualizar():
            lista.delete(*lista.get_children())
            DespesasData.cursor.execute("""
                    SELECT ID, NOME, QUANTIDADE, VALOR, CALENDARIO FROM Despesas ORDER BY ID
                    """)
            despesas = DespesasData.cursor.fetchall()
            inicio = int(inicio1.replace('/', ''))
            final = int(fim1.replace('/', ''))
            x = 0
            for i in despesas:
                z = int(despesas[x][4].replace('/', ''))
                x += 1
                if inicio <= z and z <= final:
                    lista.insert('', END, values=i)

        def OrdenarNome():
            lista.delete(*lista.get_children())
            DespesasData.cursor.execute("""
                    SELECT ID, NOME, QUANTIDADE, VALOR, CALENDARIO FROM Despesas ORDER BY NOME
                    """)
            despesas = DespesasData.cursor.fetchall()
            inicio = int(inicio1.replace('/', ''))
            final = int(fim1.replace('/', ''))
            x = 0
            for i in despesas:
                z = int(despesas[x][4].replace('/', ''))
                x += 1
                if inicio <= z and z <= final:
                    lista.insert('', END, values=i)

        def OrdenarQuantidade():
            lista.delete(*lista.get_children())
            DespesasData.cursor.execute("""
                    SELECT ID, NOME, QUANTIDADE, VALOR, CALENDARIO FROM Despesas ORDER BY QUANTIDADE
                    """)
            despesas = DespesasData.cursor.fetchall()
            inicio = int(inicio1.replace('/', ''))
            final = int(fim1.replace('/', ''))
            x = 0
            for i in despesas:
                z = int(despesas[x][4].replace('/', ''))
                x += 1
                if inicio <= z and z <= final:
                    lista.insert('', END, values=i)
        def OrdenarValor():
            lista.delete(*lista.get_children())
            DespesasData.cursor.execute("""
                    SELECT ID, NOME, QUANTIDADE, VALOR, CALENDARIO FROM Despesas ORDER BY VALOR
                    """)
            despesas = DespesasData.cursor.fetchall()
            inicio = int(inicio1.replace('/', ''))
            final = int(fim1.replace('/', ''))
            x = 0
            for i in despesas:
                z = int(despesas[x][4].replace('/', ''))
                x += 1
                if inicio <= z and z <= final:
                    lista.insert('', END, values=i)

        def OrdenarDATA():
            lista.delete(*lista.get_children())
            DespesasData.cursor.execute("""
                           SELECT ID, NOME, QUANTIDADE, VALOR, CALENDARIO FROM Despesas ORDER BY CALENDARIO
                           """)
            despesas = DespesasData.cursor.fetchall()
            inicio = int(inicio1.replace('/', ''))
            final = int(fim1.replace('/', ''))
            x = 0
            for i in despesas:
                z = int(despesas[x][4].replace('/', ''))
                x += 1
                if inicio <= z and z <= final:
                    lista.insert('', END, values=i)

        Atualizar = ttk.Button(canvas, text='  Atualizar ', width=18,command=Atualizar)
        Atualizar.place(x=12, y=8)

        OrdenarNome = ttk.Button(canvas, text='Nome', width=12,command=OrdenarNome)
        OrdenarNome.place(x=224, y=8)

        OrdenarQuantidade = ttk.Button(canvas, text='Quantidade', width=12,command=OrdenarQuantidade)
        OrdenarQuantidade.place(x=305, y=8)

        OrdernarValor = ttk.Button(canvas, text='Valor', width=12,command=OrdenarValor)
        OrdernarValor.place(x=386, y=8)

        OrdernarDATA = ttk.Button(canvas, text='Data', width=12,command=OrdenarDATA)
        OrdernarDATA.place(x=467, y=8)

        jan4.mainloop()
















JanelaPrincipal().Iniciar()