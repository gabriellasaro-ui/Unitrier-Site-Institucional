from flask import Flask, render_template

app = Flask(__name__)

# Routes
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/quem-somos')
def quem_somos():
    return render_template('quem-somos.html')

@app.route('/servicos/comercial')
def comercial():
    return render_template('comercial.html')

@app.route('/servicos/estoque')
def estoque():
    return render_template('estoque.html')

@app.route('/servicos/financeiro')
def financeiro():
    return render_template('financeiro.html')

@app.route('/servicos/pessoal-operacao')
def pessoal_operacao():
    return render_template('pessoal-operacao.html')

@app.route('/servicos/estrategico')
def estrategico():
    return render_template('estrategico.html')

@app.route('/cases')
def cases():
    return render_template('cases-sucesso.html')

@app.route('/contato')
def contato():
    return render_template('contato.html')

@app.route('/diagnostico-360')
def diagnostico_360():
    return render_template('diagnostico-360.html')

@app.route('/produtos/shelf')
def shelf():
    return render_template('software-shelf.html')

if __name__ == '__main__':
    app.run(debug=True)
