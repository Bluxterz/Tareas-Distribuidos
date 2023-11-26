import os
import wikipedia as wiki

p = [
    "Hajime Isayama",
    "Attack_on_Titan",
    "Kodansha",
    "MAPPA",
    "Wit Studio",
    "Gohan",
    "Goku",
    "Vegeta",#
    "Eren Yeager",
    "Mikasa Ackerman",
    "Armin Arlert",
    "Levi Ackerman",
    "Historia Reiss",
    "Jean Kirstein",
    "Connie Springer", 
    "Sasha Blouse",
    "Erwin Smith (Attack on Titan)",
    "Reiner Braun",
    "Annie Leonhart",
    "Zeke Yeager",
    "Pieck Finger",
    "Porco Galliard",
    "Colt Grice",
    "Falco Grice",
    "Ymir",
    "Keith Shadis",
    "Kenny Ackerman",
    "Ymir Fritz",
    "Rod Reiss",
    "Marco Bott"
]

for i in p:
    a = wiki.page(i,auto_suggest=False)
    carpeta = "carpeta1" if p.index(i) < 15 else "carpeta2"
    with open("../"+carpeta+"/"+str(p.index(i))+"wiki"+str(i.replace(" ", "_"))+".txt", "w") as f:
        f.write(str(p.index(i))+"xdxdxd")
        f.write('\n')
        f.write(a.content)
        f.write('\n')
        f.close()
    print("Escribio el archivo: "+i)