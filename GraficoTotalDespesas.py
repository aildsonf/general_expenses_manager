import tkinter

from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure

import DespesaSomaBD
from tkinter import messagebox

def GetGrafico():
    DespesaSomaBD.cursor.execute("""
                                          SELECT VALOR, CALENDARIO FROM DespesasSoma
                                          """)
    despesas = DespesaSomaBD.cursor.fetchall()
    valores = []
    datas = []
    if despesas != None:
        for x in range(len(despesas)):
            valores.append(despesas[x][0])
            datas.append((despesas[x][1]))

        root = tkinter.Tk()
        root.wm_title("VPSBank--- Visualizando Gráfico")

        fig = Figure(figsize=(5, 4), dpi=100)
        ax = fig.add_subplot(111)

        data = valores

        ind = datas  # the x locations for the groups
        width = .5

        rects1 = ax.bar(ind, data, width)

        canvas = FigureCanvasTkAgg(fig, master=root)  # A tk.DrawingArea.
        canvas.draw()
        canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

        toolbar = NavigationToolbar2Tk(canvas, root)
        toolbar.update()
        canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

        def on_key_press(event):
            print("you pressed {}".format(event.key))
            key_press_handler(event, canvas, toolbar)

        canvas.mpl_connect("key_press_event", on_key_press)

        def _quit():
            root.quit()  # stops mainloop
            root.destroy()  # this is necessary on Windows to prevent
            # Fatal Python Error: PyEval_RestoreThread: NULL tstate

        button = tkinter.Button(master=root, text="Quit", command=_quit)
        button.pack(side=tkinter.BOTTOM)

        tkinter.mainloop()
    else:
        messagebox.showwarning(title='Error na Operção', message="Valores não encontrados")

def GetGraficoPeriodo(inicio, fim):
    DespesaSomaBD.cursor.execute("""
                                          SELECT VALOR, CALENDARIO FROM DespesasSoma
                                          """)
    despesas = DespesaSomaBD.cursor.fetchall()
    valores = []
    datas = []
    print(despesas)
    inicio1 = int(inicio.replace('/', ''))
    fim1 = int(fim.replace('/', ''))
    if despesas != None:
        for x in range(len(despesas)):
            if inicio1 <= int(despesas[x][1].replace('/', '')) <= fim1:
                valores.append(despesas[x][0])
                datas.append((despesas[x][1]))
                print(valores)
                print(datas)
        root = tkinter.Tk()
        root.wm_title("VPSBank--- Visualizando Gráfico")

        fig = Figure(figsize=(5, 4), dpi=100)
        ax = fig.add_subplot(111)

        data = valores

        ind = datas  # the x locations for the groups
        width = .5

        rects1 = ax.bar(ind, data, width)

        canvas = FigureCanvasTkAgg(fig, master=root)  # A tk.DrawingArea.
        canvas.draw()
        canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

        toolbar = NavigationToolbar2Tk(canvas, root)
        toolbar.update()
        canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

        def on_key_press(event):
            print("you pressed {}".format(event.key))
            key_press_handler(event, canvas, toolbar)

        canvas.mpl_connect("key_press_event", on_key_press)

        def _quit():
            root.quit()  # stops mainloop
            root.destroy()  # this is necessary on Windows to prevent
            # Fatal Python Error: PyEval_RestoreThread: NULL tstate

        button = tkinter.Button(master=root, text="Quit", command=_quit)
        button.pack(side=tkinter.BOTTOM)

        tkinter.mainloop()
    else:
        messagebox.showwarning(title='Error na Operção', message="Valores não encontrados")











