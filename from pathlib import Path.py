from pathlib import Path

# Edite os nomes e as extensões para personalizar as categorias.
TIPOS = {
	"foto": {".jpg", ".jpeg", ".png", ".webp", ".bmp"},
	"vídeo": {".mp4", ".mov", ".avi", ".mkv"},
	"gif": {".gif"},
}

def organizar_nomes(caminho_pasta):
	pasta = Path(caminho_pasta)
	if not pasta.is_dir():
		raise NotADirectoryError(f"Pasta não encontrada: {pasta}")

	arquivos = sorted((item for item in pasta.iterdir() if item.is_file()),
					  key=lambda item: item.name.lower())
	contagens = {tipo: 0 for tipo in TIPOS}
	renomes = []

	for arquivo in arquivos:
		tipo = next((nome for nome, extensoes in TIPOS.items()
					 if arquivo.suffix.lower() in extensoes), None)
		if tipo is None:
			continue  # Extensões não configuradas não são alteradas.

		contagens[tipo] += 1
		destino = pasta / f"{tipo}_{contagens[tipo]}{arquivo.suffix}"
		if destino != arquivo:
			renomes.append((arquivo, destino))

	# Evita sobrescrever arquivos existentes que não serão renomeados.
	fontes = {origem for origem, _ in renomes}
	for _, destino in renomes:
		if destino.exists() and destino not in fontes:
			raise FileExistsError(f"O destino já existe: {destino}")

	for origem, destino in renomes:
		origem.rename(destino)
		print(f"{origem.name} -> {destino.name}")

	print("Contagem por tipo:")
	for tipo, total in contagens.items():
		print(f"{tipo}: {total}")

if __name__ == "__main__":
	organizar_nomes(input("Caminho da pasta: ").strip())
