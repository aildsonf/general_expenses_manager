package controller;

import models.ItemDespesa;
import models.Usuario;

import java.util.ArrayList;

public class Gerenciador {
    private Usuario usuario;
    private ArrayList<ItemDespesa> despesas;
    private double total;

    public Gerenciador() {
        this.usuario = null;
        this.despesas = new ArrayList<ItemDespesa>();
        this.total = 0;
    }

    public Usuario getUsuario() {
        return usuario;
    }

    public void setUsuario(Usuario usuario) {
        this.usuario = usuario;
    }

    public double getTotal() {
        return total;
    }

    public void setTotal(double total) {
        this.total = total;
    }

    public void insereUsuario(Usuario u) throws Exception {
        if(getUsuario() == null) {
            setUsuario(u);
            getUsuario();
        } else {
            throw new Exception("Já existe um usuário");
        }
    }

    public void removeUsuario() throws Exception {
        if(getUsuario() != null) {
            setUsuario(null);
            this.despesas.clear();
            setTotal(0);
        } else {
            throw new Exception("Não existe usuário");
        }
    }

    public void insereSaldo(double valor) {
        getUsuario().inserirSaldo(valor);
    }

    public void atualizaSaldo(double valor) {
        getUsuario().setSaldo(valor);
    }

    public void insereDespesa(ItemDespesa d) throws Exception {
        if(getUsuario().getSaldo() >= d.getValor()) {
            getUsuario().subtrairSaldo(d.getValor());
            this.despesas.add(d);
        } else {
            throw new Exception("Saldo Insuficiente");
        }
    }

    public boolean removeDespesa(ItemDespesa d) {
        getUsuario().inserirSaldo(d.getValor());
        return this.despesas.remove(d);
    }

    public void mostraExtrato() {
        for(ItemDespesa d : despesas) {
            System.out.println(d);
        }
    }
}
