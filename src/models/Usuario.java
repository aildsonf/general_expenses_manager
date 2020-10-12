package models;

public class Usuario {
    private String nome;
    private double saldo;

    public Usuario(String nome) {
        this.nome = nome;
        this.saldo = 0;
    }

    public String getNome() {
        return nome;
    }

    public void setNome(String nome) {
        this.nome = nome;
    }

    public double getSaldo() {
        return saldo;
    }

    public void setSaldo(double saldo) {
        this.saldo = saldo;
    }

    public void inserirSaldo(double valor) {
        this.saldo += valor;
    }

    public void subtrairSaldo(double valor) {
        this.saldo -= valor;
    }

    @Override
    public String toString() {
        return getNome() + ", $" + getSaldo();
    }
}
