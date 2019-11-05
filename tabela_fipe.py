import requests
import pandas as pd

def tabela_fipe(preco_max):
	marcas = [13,21,22,23,25,26,31,41,43,44,48,56,59,57,58]
	anos = [2013,2014,2015,2016,2017,2018]
	combustivel = [1,2,3]
	
	output = []
	for c in marcas:
			consulta_modelos = {
						"codigoTabelaReferencia": 246,
						"codigoTipoVeiculo": 1,
						"codigoMarca": c
					}
			r = requests.post(
									'http://veiculos.fipe.org.br/api/veiculos/ConsultarModelos',
									json=consulta_modelos,
									headers={
											'Host': 'veiculos.fipe.org.br',
											'Referer': 'http://veiculos.fipe.org.br/'
											}
									)
			
			for d in r.json()['Modelos']: #todos os modelos da marca
					
	
					for i in anos:
							for j in combustivel:
													anoJson = f"{i}-{j}"
													consulta_valor = {
															"codigoTabelaReferencia": 246, #novembro/19
															"codigoTipoVeiculo": 1, #automovel (nao moto ou caminhao)
															"codigoMarca": c,
															"ano": anoJson,
															"codigoTipoCombustivel": j,
															"anoModelo": i,
															"codigoModelo": d['Value'],
															"tipoConsulta": "tradicional"
																	}
													
													r = requests.post(
															'http://veiculos.fipe.org.br/api/veiculos/ConsultarValorComTodosParametros',
															json=consulta_valor,
															headers={
															'Host': 'veiculos.fipe.org.br',
															'Referer': 'http://veiculos.fipe.org.br/'
															}
															)
											
													if('Valor' in r.json()):
																	print(str(r.json()['Marca']) +" "+ str(r.json()['Modelo']) +" "+ str(r.json()['AnoModelo']) \
																											+" "+ str(r.json()['Combustivel']) +" "+ str(r.json()['Valor']))
																	output.append(r.json())
	
	
	dfCarros = pd.DataFrame(output)
	
	dfCarros['value_fix'] = dfCarros['Valor'].apply(lambda x: x.replace("R$ ",""))
	dfCarros['value_fix'] = dfCarros['value_fix'].apply(lambda x: x.replace(".",""))
	dfCarros['value_fix'] = dfCarros['value_fix'].apply(lambda x: x.replace(",","."))
	dfCarros['value_fix'] = dfCarros['value_fix'].astype(float)
	
	return dfCarros.loc[dfCarros['value_fix']<preco_max].sort_values(by=['AnoModelo','value_fix'], ascending=(False,True)).head(20)
