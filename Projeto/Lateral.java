package projeto;

import java.util.ArrayList;
import java.util.Map;

public class Lateral extends Jogador {
    private int cruzamento;
    private int drible;

    public Lateral() {
        super();
        this.cruzamento = 0;
        this.drible = 0;
    }

    public Lateral(String nom, String eq, int ide, ArrayList<String> hist, Map<String,Integer> ats, int cr, int dr) {
        super(nom, eq,ide, hist, ats);
        this.cruzamento = cr;
        this.drible = dr;
    }

    public Lateral(Lateral d) {
        super(d);
        this.cruzamento = d.cruzamento;
        this.drible = d.drible;
    }

    public Lateral clone() {
        return new Lateral(this);
    }

    public boolean equals(Object o) {
        if (this == o) return true;

        if (o == null || o.getClass() != this.getClass()) return false;

        Lateral l = (Lateral) o;
        return super.equals(o) && this.cruzamento == l.cruzamento && this.drible == l.drible;
    }

    public String toString() {
        return super.toString() + "\nCorte: " + this.cruzamento + "\nIntersecçao: " + this.drible + "\n";
    }

    public int calculaOverall() {
        return 0;
    }

    public void setCruzamento(int cr) {
        this.cruzamento = cr;
    }
    public int getCruzamento() {
        return this.cruzamento;
    }
    public void setDrible(int dr) {
        this.drible = dr;
    }
    public int getDrible() {
        return this.drible;
    }
}
