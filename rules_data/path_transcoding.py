path_transcoding = {
    "à la maison": "_embedded.documents[0].content.collectedData.location.isAtHome",
    "autoroute": "_embedded.documents[0].content.collectedData.location.isOnMotorway",
    "type d'incident véhicule": "_embedded.documents[0].content.botDialogSlot.breakdown_vs_accident",
    "effet client véhicule": "_embedded.documents[0].content.botDialogSlot.breakdown_generator_fact",
    "contexte final": "_embedded.documents[0].content.botDialogSlot.final_context",
    "assureur" : "_embedded.documents[0].content.botDialogSlot.assureur",
    "benef insultant": "_embedded.documents[0].content.collectedData.requestSentiment.isInsult",
    "nom de la rue": "_embedded.documents[0].content.collectedData.requestGeneralInformation.address.road",
    "ville": "_embedded.documents[0].content.collectedData.requestGeneralInformation.address.city",
    "departement": "_embedded.documents[0].content.collectedData.requestGeneralInformation.address.department",
    "type de demande": "_embedded.documents[0].content.collectedData.request.requestType",
    "is abuser": "_embedded.documents[0].content.collectedData.requestGeneralInformation.isAbuser",
    "intent":"_embedded.documents[0].content.callbotPathData.conversation.mainIntent"
}