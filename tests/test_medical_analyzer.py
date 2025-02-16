import pytest
from src.backend.medical_analyzer import MedicalAnalyzer
from src.backend.graph_navigator import MedGraphNavigator

@pytest.fixture
def analyzer():
    """Create a test analyzer instance with sample data"""
    nav = MedGraphNavigator()
    nav.load_synthea_data()
    return MedicalAnalyzer(nav.graph)

def test_treatment_patterns(analyzer):
    """Test treatment pattern analysis"""
    patterns = analyzer.analyze_treatment_patterns("Type 2 Diabetes")
    assert patterns is not None
    assert len(patterns) > 0

def test_similar_patients(analyzer):
    """Test patient similarity analysis"""
    similar = analyzer.find_similar_patients("P1", num_similar=5)
    assert similar is not None
    assert len(similar) <= 5

def test_risk_factors(analyzer):
    """Test risk factor prediction"""
    risks = analyzer.predict_risk_factors("Heart Disease")
    assert risks is not None
    assert isinstance(risks, dict)
