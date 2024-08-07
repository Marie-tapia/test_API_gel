from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from serializers import CommentSerializer
from .dictionaries import dictionaries
import nltk
from nltk.tokenize import word_tokenize
import string
import unicodedata

nltk.download('punkt')
nltk.download('stopwords')

class CommentView(APIView):
    def post(self, request):
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            comments = serializer.validated_data['comments']
            processed_comments = [self.process_comment(comment) for comment in comments]
            return Response(processed_comments, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def clean_text(self, text):
        text = text.lower()
        print(f"After lowercasing: {text}")
        text = ''.join(c for c in unicodedata.normalize('NFD', text) if not unicodedata.combining(c))
        print(f"After removing diacritics: {text}")
        translation_table = str.maketrans(string.punctuation, ' ' * len(string.punctuation))
        text = text.translate(translation_table)
        print(f"After punctuation removal: {text}")
        text = ''.join(c for c in text if not c.isdigit())
        print(f"After removing digits: {text}")
        return text

    def remove_stopwords_tokenisation(self, text):
        words = word_tokenize(text)
        print(f"After tokenization: {words}")
        return words

    def process_comment(self, comment):
        print(f"Original comment: {comment}")
        comment = self.clean_text(comment)
        tokens = self.remove_stopwords_tokenisation(comment)
        print(f"Final tokens: {tokens}")
        scores = {
            "VSS": self.remonter_harcelement_vss(tokens, dictionaries["dico_racine_harc"], dictionaries["dico_harcelement"]),
            "droit": self.remonter_commentaire(tokens, dictionaries["dico_manque_droit"]),
            "encadrement": self.remonter_commentaire(tokens, dictionaries["dico_manque_encadrement"]),
            "pedagogie": self.remonter_commentaire(tokens, dictionaries["dico_manque_pedagogie"]),
        }
        print(f"Scores: {scores}")
        return scores

    def remonter_harcelement_vss(self, data_com, dictionnaire_racine, dictionnaire):
        score_sum = 0
        nb_mot_assos = 0
        nb_valeur1_ngram = 0
        nb_valeur1_racine = 0
        racines_traite = set()
        mot_traites = set()

        for token in data_com:
            for rac in dictionnaire_racine:
                if token.startswith(rac):
                    print(f"Matched racine: {rac} with value: {dictionnaire_racine[rac]}")
                    score_sum += dictionnaire_racine[rac]
                    nb_mot_assos += 1
                    if dictionnaire_racine[rac] == 1 and rac not in racines_traite:
                        nb_valeur1_racine += 1
                        racines_traite.add(rac)
                    break

        ngram_lengths = range(1, 6)

        for n in ngram_lengths:
            for i in range(len(data_com) - n + 1):
                ngram = tuple(data_com[i:i + n])
                if ngram in dictionnaire:
                    print(f"Matched ngram: {ngram} with value: {dictionnaire[ngram]}")
                    score_sum += dictionnaire[ngram]
                    nb_mot_assos += 1
                    if dictionnaire[ngram] == 1 and ngram not in mot_traites:
                        nb_valeur1_ngram += 1
                        mot_traites.add(ngram)

        if nb_mot_assos == 0:
            return 0

        score = score_sum / nb_mot_assos
        bonus = nb_valeur1_racine + nb_valeur1_ngram
        score += bonus
        score = round(score, 3)

        return score

    def remonter_commentaire(self, data_com, dictionnaire):
        score_sum = 0
        nb_mot_assos = 0
        nb_valeur1_ngram = 0
        mot_traites = set()

        ngram_lengths = range(1, 6)

        for n in ngram_lengths:
            for i in range(len(data_com) - n + 1):
                ngram = tuple(data_com[i:i + n])
                if ngram in dictionnaire:
                    print(f"Matched ngram: {ngram} with value: {dictionnaire[ngram]}")
                    score_sum += dictionnaire[ngram]
                    nb_mot_assos += 1
                    if dictionnaire[ngram] == 1 and ngram not in mot_traites:
                        nb_valeur1_ngram += 1
                        mot_traites.add(ngram)

        if nb_mot_assos == 0:
            return 0

        score = score_sum / nb_mot_assos
        bonus = nb_valeur1_ngram
        score += bonus
        score = round(score, 3)

        return score
