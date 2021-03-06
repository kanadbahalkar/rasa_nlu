from rasa_nlu.emulators import NoEmulator


class LUISEmulator(NoEmulator):
    def __init__(self):
        super(LUISEmulator, self).__init__()
        self.name = 'luis'

    def _top_intent(self, data):
        if data.get("intent"):
            return {
                "intent": data["intent"]["name"],
                "score": data["intent"]["confidence"]
            }
        else:
            return None

    def _ranking(self, data):
        if data.get("intent_ranking"):
            return [{"intent": el["intent"], "score": el["confidence"]} for el in data["intent_ranking"]]
        else:
            return [self._top_intent(data)]

    def normalise_response_json(self, data):
        top_intent = self._top_intent(data)
        ranking = self._ranking(data)
        return {
            "query": data["text"],
            "topScoringIntent": top_intent,
            "intents": ranking,
            "entities": [
                {
                    "entity": e["value"],
                    "type": e["entity"],
                    "startIndex": None,
                    "endIndex": None,
                    "score": None
                } for e in data["entities"]
                ]
        }
