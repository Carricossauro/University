# Considere n=1431702961131339621602945101050088245802771644687686106472404992618656781417216251296575852739319584928520070989102317406096771341195807540255351846662720304620283140579998725212022478694288443,
# o produto de dois primos p e q, com p<q, é
# phi_n=1431702961131339621602945101050088245793639679386713169093313712250573769060652354811397118799813658291947433707988011985679885048571032964071342275971679191493672348651555118274559858896490208
# entao p,q são

crack_rsa(n,phi_n)


# De uma chave pública RSA (n,e)=(5746373959926501631, 816210188025244429) sabe-se que
# p=1434802597 divide n. Então o expoente de decifração, d, é igual a

q = n/p
phi_n = (p-1)*(q-1)
d = inverse_mod(e,phi_n)


# Considere o natural n=121

7 in all_prim_roots(121)


# Para n=7*11 e a=60*10^6+3 , o resto da divisão inteira de 3^a por n é

Mod(3^a,n)


# Dada a chave pública RSA com (n,e) = (1020503581,180933103)
# , a cifração de mens=1234 é encrypt(mens,n,e)

encrypt(1234,1020503581,180933103)

# Considere n=2^30-1 m=2^29-1 e o isomorfismo f de anéis Zₙₘ 
# para Zₙ x Zₘ. A imagem recíproca de a,b = (402374628, 220354304) é

crt([a,b],[n,m])