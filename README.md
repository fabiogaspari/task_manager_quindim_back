# Gerenciador de Tarefas Quindim (backend)
Para esse microserviço do backend, foi utilizada a linguagem Python com o framework Flask e os bancos de dados mongodb e redis.

# Para rodar o projeto
1. Crie uma pasta nova e adicione os dois projetos
   1. Baixe esse projeto e o do frontend nessa pasta (https://github.com/fabiogaspari/task_manager_quindim)
2. Rode o arquivo docker-compose.yml que está em ambos os projetos, na pasta em que os projetos estão baixados. Ex.:
   1. pasta_pai/task_manager_quindim_back
   2. pasta_pai/task_manager_quindim
   3. rodar o docker-compose.yml na pasta = pasta_pai

# Utilizarios
1. Para desenvolver o projeto do backend, primeiro foi desenvolvido o Diagrama de Entidade e Relacionamento, com a ferramenta drawia. Um arquivo exportado desse diagrama, no formado .png, se encontra na raiz do projeto no github.

# PROJETO AINDA EM ANDAMENTO
## Próximos passos
2. Desenvolver os testes unitários
3. Desenvolver arquivo bash para criação das imagens Docker
4. Desenvolver endpoint de métricas
