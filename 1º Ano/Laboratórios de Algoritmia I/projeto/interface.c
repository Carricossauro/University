/**
@file interface.c
Definição das funçôes que fornecem a ligação ao jogador
*/

#include "dados.h"
#include "logica.h"
#include "interface.h"
#include "listas.h"
#include <limits.h>
#include <stdio.h>
#include <string.h>
#include <bits/types/FILE.h>
#include <stdlib.h>
#include "minimax.h"

/** Definição de um buf size para ser usado mais tarde */
#define BUF_SIZE 1024

void mostrar_tabuleiro(ESTADO *e, FILE *jogo) {
    for (int i = 7; i >= 0; i--) {
        for (int k = 0; k < 8; k++) {
            if (i == 0 && k == 0)
                fprintf(jogo, "1");
            else if (i == 7 && k == 7)
                fprintf(jogo, "2");
            else
                fprintf(jogo, ((obter_casa(e, k, i) == PRETA) ? "#" : ((obter_casa(e, k, i) == BRANCA) ? "*" : ".")));
        }
        fprintf(jogo, "\n");
    }
}

void ler (char *ficheiro, ESTADO *e)
{
    FILE *jogo;
    jogo = fopen(ficheiro, "r");
    char linha[25];
    char c1, c2;
    int n1, n2;
    char str[25];

    free(e);
    e = inicializar_estado();

    for (int i = 7; i >= 0; i--)
    {
        if(fgets(linha, 25, jogo)) {
            recebelinha(linha, i, e);
        }
    }

    if(fgets(linha, 25, jogo)) {
        while (fgets(linha, 25, jogo) != NULL) {
            if (sscanf(linha, "%s %c%d %c%d", str, &c1, &n1, &c2, &n2) == 5) {
                recebe_jogadas(e, c1, n1);
                recebe_jogadas(e, c2, n2);
            } else if (sscanf(linha, "%s %c%d", str, &c1, &n1) == 3) {
                recebe_jogadas(e, c1, n1);
            }
        }
    }

    fclose(jogo);
}

void gravar (char *ficheiro, ESTADO *e)
{
    muda_inc(e, obter_jogador_atual(e));
    pos(e, obter_numero_de_movimentos(e));
    FILE *jogo;
    jogo = fopen(ficheiro, "w");
    mostrar_tabuleiro(e, jogo);
    fprintf(jogo, "\n");
    movs(jogo, e);
    fclose(jogo);
    muda_inc(e, 0);
}

void mostrar_prompt(ESTADO *e){
    printf("# %02d",conta_comandos(e));
    printf(" PL%d",obter_jogador_atual(e));
    printf(" (%d)> ",obter_numero_de_movimentos(e));
}

void movs(FILE *jogo, ESTADO *e){
    pos(e, obter_numero_de_movimentos(e));
    char *str;
    for (int i = 0; i < obter_numero_de_movimentos(e); i++) {
        if (jogada_existe(e, i, 1)) {
            fprintf(jogo, "%02d: %s", i+1, (str = obter_jogada(e, i, 1)));
            free(str);
        } else break;

        if (jogada_existe(e, i, 2)) {
            fprintf(jogo, " %s\n", (str = obter_jogada(e, i, 2)));
            free(str);
        } else break;
    }
}

void jog(ESTADO *e){
    float d = INT_MAX;

    COORDENADA c, origem, *a;

    LISTA l = criar_lista();
    l = potenciais_jogadas(e, l);

    LISTA t = l;

    if (obter_jogador_atual(e) == 1){
        origem.linha = 0;
        origem.coluna = 0;
    }
    else {
        origem.linha = 7;
        origem.coluna = 7;
    }

    while (!lista_esta_vazia(t)){
        a = (COORDENADA*) devolve_cabeca(t);
        distancia(*a, origem);
        if (distancia(*a, origem) < d){
            d = distancia(*a, origem);
            c = *a;
        }
        t = proximo(t);
    }

    jogar(e, c);

    while (!lista_esta_vazia(l)) {
        l = remove_cabeca(l);
    }
}

void jog2(ESTADO *e){
    COORDENADA c = obter_ultima_jogada(e), *a, *p = NULL;
    float x = INT_MIN;
    float y;

    if (obter_jogador_atual(e) == 1) {
        for (int i = obter_linha(c) - 1; i <= obter_linha(c) + 1 ; i++) {
            for (int j = obter_coluna(c) - 1; j <= obter_coluna(c) + 1 ; j++) {
                a = malloc(sizeof(COORDENADA));
                a->linha = i;
                a->coluna = j;
                if((y = Minimax(6, *a, e, 1)) > x && casa_esta_livre(e, *a)){
                    p = a;
                    x = y;
                }else free(a);
            }
        }
    } else {
        for (int i = obter_linha(c) + 1; i >= obter_linha(c) - 1; i--) {
            for (int j = obter_coluna(c) + 1; j >= obter_coluna(c) - 1 ; j--) {
                a = malloc(sizeof(COORDENADA));
                a->linha = i;
                a->coluna = j;
                if((y = Minimax(6, *a, e, 1)) > x && casa_esta_livre(e, *a)){
                    p = a;
                    x = y;
                }else free(a);
            }
        }
    }
    if (x != 1) {
        if(p != NULL){
            jogar(e, *p);
            free(p);
        }
    } else {
        jog(e);
    }

}

int interpretador(ESTADO *e) {
    char linha[BUF_SIZE];
    char col[2], lin[2];
    char comando[10];
    char ficheiro[BUF_SIZE];

    mostrar_tabuleiro(e, stdout);
    mostrar_prompt(e);
    if(fgets(linha, BUF_SIZE, stdin) == NULL)
        return 0;

    if(strlen(linha) == 3 && sscanf(linha, "%[a-h]%[1-8]", col, lin) == 2) {
        verifica_njogadas(e);
        COORDENADA coord = {*col - 'a', *lin - '1'};
        jogar(e, coord);
        add_comando(e);
    }
    else if(!strcmp(linha, "Q\n"))
    {
        return 0;
    }
    else if(sscanf(linha, "%s %s", comando, ficheiro) == 2)
    {
        if(!strcmp(comando, "ler"))
        {
            ler(ficheiro, e);
            add_comando(e);
        }
        else if (!strcmp(comando, "gr"))
        {
            gravar(ficheiro, e);
            add_comando(e);
        }
        else if (!strcmp(comando, "pos"))
        {
            muda_inc(e, obter_jogador_atual(e));
            pos(e, atoi(ficheiro));
            add_comando(e);
            putchar('\n');
        }
    }
    else if(sscanf(linha, "%s", comando) == 1)
    {
        if (!strcmp(comando, "movs")) {

            muda_inc(e, obter_jogador_atual(e));
            movs(stdout, e);
            add_comando(e);
            muda_inc(e, 0);
            putchar('\n');
        }
        else if (!strcmp(comando, "jog")) {
            jog(e);
            add_comando(e);
            putchar('\n');
        }
        else if (!strcmp(comando, "jog2")) {
            jog2(e);
            add_comando(e);
            putchar('\n');
        }
        else if (!strcmp(comando, "retira")) {
            retirar_ultima_jogada(e);
            add_comando(e);
            putchar('\n');
        }
    }
    return 1;
}