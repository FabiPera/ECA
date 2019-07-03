from PIL import Image
import img2pdf

den=Image.open("Density.png").convert("RGB")
den.save("Density.png")
den.close()
ent=Image.open("Entropy.png").convert("RGB")
ent.save("Entropy.png")
ent.close()
lyap=Image.open("LyapunovExp.png").convert("RGB")
lyap.save("LyapunovExp.png")
lyap.close()

images=["Simulation.png", "DamageSimulation.png", "DamageCone.png", "Density.png", "Entropy.png", "LyapunovExp.png"]
with open("PhenAnalysis.pdf", "wb") as f:
	f.write(img2pdf.convert(images))

