
from typing import List, Dict, Tuple, Optional, Set
from enum import Enum
import re
from dataclasses import dataclass

class ChordQuality(Enum):
    MAJOR = "major"
    MINOR = "minor"
    DIMINISHED = "diminished"
    AUGMENTED = "augmented"
    DOMINANT = "dominant7"
    MAJOR7 = "major7"
    MINOR7 = "minor7"
    HALF_DIMINISHED = "half_diminished"
    DIMINISHED7 = "diminished7"
    SUSPENDED4 = "suspended4"
    SUSPENDED2 = "suspended2"

class Function(Enum):
    TONIC = "T"
    SUBDOMINANT = "S"
    DOMINANT = "D"
    SECONDARY_DOMINANT = "V/x"
    DIMINISHED = "dim"
    SUBSTITUTE = "sub"

@dataclass
class Chord:
    root: str
    quality: ChordQuality
    extensions: List[str] = None
    bass: str = None
    function: Function = None
    roman_numeral: str = None

    def __post_init__(self):
        if self.extensions is None:
            self.extensions = []

@dataclass  
class Scale:
    root: str
    mode: str
    notes: List[str]

class MusicTheoryEngine:
    def __init__(self):
        # Notas cromáticas (método Ian Guest)
        self.chromatic_notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
        self.enharmonic_map = {
            'C#': 'Db', 'D#': 'Eb', 'F#': 'Gb', 
            'G#': 'Ab', 'A#': 'Bb'
        }

        # Intervalos (base Berklee)
        self.intervals = {
            0: 'P1',   # Unisson
            1: 'm2',   # Segunda menor
            2: 'M2',   # Segunda maior  
            3: 'm3',   # Terça menor
            4: 'M3',   # Terça maior
            5: 'P4',   # Quarta justa
            6: 'TT',   # Trítono
            7: 'P5',   # Quinta justa
            8: 'm6',   # Sexta menor
            9: 'M6',   # Sexta maior
            10: 'm7',  # Sétima menor
            11: 'M7'   # Sétima maior
        }

        # Modos (Ian Guest Vol. 3)
        self.modes = {
            'ionian': [0, 2, 4, 5, 7, 9, 11],      # Modo jônio (maior)
            'dorian': [0, 2, 3, 5, 7, 9, 10],      # Modo dórico
            'phrygian': [0, 1, 3, 5, 7, 8, 10],    # Modo frígio
            'lydian': [0, 2, 4, 6, 7, 9, 11],      # Modo lídio
            'mixolydian': [0, 2, 4, 5, 7, 9, 10],  # Modo mixolídio
            'aeolian': [0, 2, 3, 5, 7, 8, 10],     # Modo eólio (menor natural)
            'locrian': [0, 1, 3, 5, 6, 8, 10]      # Modo lócrio
        }

        # Funções harmônicas (baseado Ian Guest)
        self.harmonic_functions = {
            'I': Function.TONIC,
            'ii': Function.SUBDOMINANT,
            'iii': Function.TONIC,
            'IV': Function.SUBDOMINANT,
            'V': Function.DOMINANT,
            'vi': Function.TONIC,
            'vii°': Function.DOMINANT
        }

    def parse_chord(self, chord_symbol: str) -> Chord:
        """Parse chord symbol usando metodologia Ian Guest"""
        # Regex para parsing de acordes
        chord_pattern = r'^([A-G][#b]?)([^/]*?)(?:/([A-G][#b]?))?$'
        match = re.match(chord_pattern, chord_symbol.strip())

        if not match:
            raise ValueError(f"Chord symbol inválido: {chord_symbol}")

        root = match.group(1)
        quality_str = match.group(2) or ""
        bass = match.group(3)

        # Determinar qualidade do acorde
        quality = self._determine_chord_quality(quality_str)
        extensions = self._parse_extensions(quality_str)

        return Chord(
            root=root,
            quality=quality,
            extensions=extensions,
            bass=bass
        )

    def _determine_chord_quality(self, quality_str: str) -> ChordQuality:
        """Determina qualidade do acorde baseado no string"""
        quality_str = quality_str.lower()

        if 'm7' in quality_str:
            return ChordQuality.MINOR7
        elif 'maj7' in quality_str or 'M7' in quality_str:
            return ChordQuality.MAJOR7
        elif '7' in quality_str:
            return ChordQuality.DOMINANT
        elif 'm' in quality_str:
            return ChordQuality.MINOR
        elif 'dim' in quality_str:
            return ChordQuality.DIMINISHED
        elif 'aug' in quality_str or '+' in quality_str:
            return ChordQuality.AUGMENTED
        elif 'sus4' in quality_str:
            return ChordQuality.SUSPENDED4
        elif 'sus2' in quality_str:
            return ChordQuality.SUSPENDED2
        else:
            return ChordQuality.MAJOR

    def _parse_extensions(self, quality_str: str) -> List[str]:
        """Parse extensões do acorde"""
        extensions = []

        # Procurar por tensões (9, 11, 13)
        tension_pattern = r'(9|11|13|#11|b13)'
        tensions = re.findall(tension_pattern, quality_str)
        extensions.extend(tensions)

        return extensions

    def analyze_chord_progression(self, chord_symbols: List[str], key: str = 'C') -> List[Dict]:
        """Analisa progressão harmônica completa"""
        analysis = []

        for chord_symbol in chord_symbols:
            chord = self.parse_chord(chord_symbol)

            # Análise harmônica
            roman_numeral = self._get_roman_numeral(chord, key)
            function = self._determine_function(roman_numeral)

            chord.roman_numeral = roman_numeral
            chord.function = function

            analysis.append({
                'chord_symbol': chord_symbol,
                'chord': chord,
                'roman_numeral': roman_numeral,
                'function': function.value,
                'tensions_available': self._get_available_tensions(chord, key),
                'scales_recommended': self._recommend_scales(chord, key)
            })

        return analysis

    def _get_roman_numeral(self, chord: Chord, key: str) -> str:
        """Converte acorde para algarismo romano"""
        # Calcular intervalo da fundamental para a tônica
        key_index = self.chromatic_notes.index(key)
        chord_index = self.chromatic_notes.index(chord.root)
        interval = (chord_index - key_index) % 12

        # Mapear para algarismo romano
        roman_map = {
            0: 'I', 2: 'II', 4: 'III', 5: 'IV',
            7: 'V', 9: 'VI', 11: 'VII'
        }

        base_roman = roman_map.get(interval, 'bII')  # Default para acordes alterados

        # Ajustar para menor/diminuto
        if chord.quality in [ChordQuality.MINOR, ChordQuality.MINOR7]:
            base_roman = base_roman.lower()
        elif chord.quality == ChordQuality.DIMINISHED:
            base_roman = base_roman.lower() + '°'

        return base_roman

    def _determine_function(self, roman_numeral: str) -> Function:
        """Determina função harmônica"""
        base_roman = roman_numeral.replace('°', '').upper()
        return self.harmonic_functions.get(base_roman, Function.SUBSTITUTE)

    def _get_available_tensions(self, chord: Chord, key: str) -> List[str]:
        """Tensões disponíveis por acorde (método Ian Guest)"""
        tensions_map = {
            ChordQuality.MAJOR7: ['9', '11', '13'],
            ChordQuality.MINOR7: ['9', '11', '13'],
            ChordQuality.DOMINANT: ['9', '11', '13', 'b13', '#11'],
            ChordQuality.HALF_DIMINISHED: ['9', '11', 'b13']
        }

        return tensions_map.get(chord.quality, [])

    def _recommend_scales(self, chord: Chord, key: str) -> List[str]:
        """Recomenda escalas para improvisação"""
        scale_recommendations = {
            ChordQuality.MAJOR7: ['ionian', 'lydian'],
            ChordQuality.MINOR7: ['dorian', 'aeolian'],
            ChordQuality.DOMINANT: ['mixolydian', 'altered'],
            ChordQuality.HALF_DIMINISHED: ['locrian']
        }

        return scale_recommendations.get(chord.quality, ['chromatic'])

    def suggest_chord_substitutions(self, chord: Chord, key: str) -> List[str]:
        """Sugestões de substituição harmônica (Ian Guest Vol. 2)"""
        substitutions = []

        if chord.quality == ChordQuality.DOMINANT:
            # Substituições de dominante
            root_index = self.chromatic_notes.index(chord.root)
            tritone_sub = self.chromatic_notes[(root_index + 6) % 12]
            substitutions.append(f"{tritone_sub}7")

        elif chord.function == Function.TONIC:
            # Substitutos da tônica
            if chord.quality == ChordQuality.MAJOR:
                substitutions.extend([f"{chord.root}6", f"{chord.root}maj9"])

        return substitutions

    def validate_voice_leading(self, progression: List[str]) -> Dict:
        """Valida condução de vozes"""
        issues = []
        suggestions = []

        for i in range(len(progression) - 1):
            current = self.parse_chord(progression[i])
            next_chord = self.parse_chord(progression[i + 1])

            # Verificar movimento de fundamentais
            current_root = self.chromatic_notes.index(current.root)
            next_root = self.chromatic_notes.index(next_chord.root)
            interval = abs(next_root - current_root)

            if interval > 6:  # Movimento maior que trítono
                issues.append(f"Movimento de fundamental muito amplo: {progression[i]} → {progression[i+1]}")
                suggestions.append("Considere usar inversão ou acorde de passagem")

        return {
            'is_valid': len(issues) == 0,
            'issues': issues,
            'suggestions': suggestions
        }
