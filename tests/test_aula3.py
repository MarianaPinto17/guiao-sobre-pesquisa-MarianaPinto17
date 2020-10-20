import pytest
from cidades import SearchProblem, SearchTree, cidades_portugal

@pytest.fixture
def braga_faro():
    return SearchProblem(cidades_portugal,'Braga','Faro')

def test_exercicio1(braga_faro):
    t = SearchTree(braga_faro,'depth')

    assert t.search() == ['Braga', 'Porto', 'Agueda', 'Aveiro', 'Coimbra', 'Leiria', 'Castelo Branco', 'Santarem', 'Lisboa', 'Evora', 'Beja', 'Faro']

def test_exercicio2(braga_faro):
    t = SearchTree(braga_faro, 'depth')

    assert t.open_nodes[-1].depth == 0
    t.search()
    assert t.solution.depth == 11

def test_exercicio3(braga_faro):
    t = SearchTree(braga_faro, 'depth')

    t.search()

    assert t.length() == 11

def test_exercicio4(braga_faro):
    t = SearchTree(braga_faro, 'depth')

    assert t.search(limit=9) == ['Braga', 'Porto', 'Agueda', 'Aveiro', 'Coimbra', 'Leiria', 'Santarem', 'Lisboa', 'Beja', 'Faro']

    assert t.length() <= 9

def test_exercicio5(braga_faro):
    t = SearchTree(braga_faro, 'depth')

    assert t.search() == ['Braga', 'Porto', 'Agueda', 'Aveiro', 'Coimbra', 'Leiria', 'Castelo Branco', 'Santarem', 'Lisboa', 'Evora', 'Beja', 'Faro']
    assert t.terminals == 18
    assert t.non_terminals == 12

    t = SearchTree(braga_faro, 'depth')

    assert t.search(limit=9) == ['Braga', 'Porto', 'Agueda', 'Aveiro', 'Coimbra', 'Leiria', 'Santarem', 'Lisboa', 'Beja', 'Faro']
    assert t.terminals == 11
    assert t.non_terminals == 59 

def test_exercicio6(braga_faro):
    t = SearchTree(braga_faro, 'depth')

    assert t.search() == ['Braga', 'Porto', 'Agueda', 'Aveiro', 'Coimbra', 'Leiria', 'Castelo Branco', 'Santarem', 'Lisboa', 'Evora', 'Beja', 'Faro']
    assert t.avg_ramification == 29/12
