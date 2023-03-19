# Image resizer API

Este projeto tem como objetivo implementar uma API REST em Python que recebe uma imagem e envia a imagem através de uma fila para uma segunda aplicação que a redimensiona para o tamanho de 384x384.

## Como executar?

Execute o seguinte comando para criar a imagem Docker:

    docker build -t image-resizer .

Execute o seguinte comando para iniciar os contêineres:

    docker-compose up

Isso iniciará o servidor Flask e o RabbitMQ. A API estará disponível em http://localhost:5000/api/resize-image.

Para testar a API, envie uma imagem para a URL http://localhost:5000/api/resize-image utilizando o método POST.
Ao enviar a imagem, a API irá salvá-la em um arquivo no diretório `images` e enviará uma mensagem para a fila `image_queue` do RabbitMQ.

## Perguntas sobre a arquitetura

### Como mudar a arquitetura para o tamanho da imagem ser parametrizável?

Se o tamanho do redimensionamento for parametrizável, uma abordagem possível seria incluir um parâmetro `size` na requisição POST da API e passar esse parâmetro para a fila do RabbitMQ. A segunda aplicação, ao receber a mensagem da fila, usaria o parâmetro `size` para redimensionar a imagem para o tamanho desejado.

### Qual a complexidade da arquitetura?

O redimensionamento de uma imagem usando a biblioteca OpenCV tem complexidade O(n), onde `n` é o número de pixels na imagem. 

A API REST e a fila do RabbitMQ têm complexidade O(1) em termos de tempo de processamento, pois cada requisição ou mensagem na fila é processada em tempo constante. Esse tempo é multiplicado por uma constante `C`, no qual `C` é o número de filas executando.

### É possível melhorar a performance da solução e como as melhorias impactam a leitura e manutenção do código?

Sim, é possível melhorar a performance da solução, principalmente no que se refere ao tempo de processamento do redimensionamento da imagem. Algumas possíveis melhorias são:

- Paralelização do redimensionamento de imagens, com controle de concorrência, de forma a utilizar melhor os recursos disponíveis no sistema, como múltiplos núcleos de CPU;

- Uso de técnicas de pré-processamento de imagem, como remoção de ruídos, para reduzir o tamanho da imagem antes de aplicar o redimensionamento, diminuindo assim o tempo de processamento.

O maior impacto na manutenção do código se deve à implementação de uma estrutura de threads e controle de concorrência (como semáforos, por exemplo), que demanda um bom conhecimento técnico de processos e arquitetura do desenvolvedor responsável.

### De que forma seria possível escalar o sistema?

Uma das maneiras de escalar o sistema é aumentar o número de instâncias do serviço da API REST através de Kubernetes e/ou Terraform, orquestrando a execução de várias instâncias da API em diferentes contêineres. As ferramentas de orquestração de contâineres também permitem criar mais instâncias dos workers do RabbitMQ e balanceam a carga entre elas. Além disso, é possível otimizar o desempenho da solução fazendo o cache das imagens redimensionadas em um sistema de armazenamento em cache.