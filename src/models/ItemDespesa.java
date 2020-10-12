package models;

public class ItemDespesa {
    private String nome;
    private double valor;
    private TipoDespesa tipoDespesa;
    private String date; // mudar para datetime

    public ItemDespesa(String nome, double valor, TipoDespesa tipoDespesa, String date) {
        this.nome = nome;
        this.valor = valor;
        this.tipoDespesa = tipoDespesa;
        this.date = date;
    }

    public String getNome() {
        return nome;
    }

    public void setNome(String nome) {
        this.nome = nome;
    }

    public double getValor() {
        return valor;
    }

    public void setValor(double valor) {
        this.valor = valor;
    }

    public TipoDespesa getTipoDespesa() {
        return tipoDespesa;
    }

    public void setTipoDespesa(TipoDespesa tipoDespesa) {
        this.tipoDespesa = tipoDespesa;
    }

    public String getDate() {
        return date;
    }

    public void setDate(String date) {
        this.date = date;
    }

    @Override
    public String toString() {
        return getNome() + ", $" + getValor();
    }
}
