# Ergasia2_e18012_Arvaniti_Maria
![Python](https://img.shields.io/badge/Python-v^3.8.5-blue.svg?logo=python&longCache=true&logoColor=white&colorB=5e81ac&style=flat-square&colorA=4c566a)
![Flask](https://img.shields.io/badge/Flask-v^1.1.2-blue.svg?longCache=true&logo=flask&style=flat-square&logoColor=white&colorB=5e81ac&colorA=4c566a)
![MongoDB](https://img.shields.io/badge/MongoDB-v%5E4.4-red.svg?longCache=true&style=flat-square&logo=scala&logoColor=white&colorA=4c566a&colorB=bf616a)
## Εισαγωγή
Το συγκεκριμένο project αφορά το εργαστήριο του μαθήματος «(ΨΣ-152) Πληροφοριακά Συστήματα» του τμήματος Ψηφιακών Συστημάτων του Πανεπιστημίου Πειραιώς και πραγματοποιήθηκε ως μέρος της εξαμηνιαίας εργασίας. Κάνοντας χρήση Python και Flask υλοποιήθηκε web service το οποίο παρέχει τα απαραίτητα endpoint στους χρήστες του, ώστε να μπορούν να εκτελεστούν ορισμένες λειτουργίες. Το web service συνδέεται με ένα container της MongoDB. Τέλος, το web service έγινε  containerized με χρήση Dockerfile και docker-compose ώστε το web service και η MongoDB να τρέχουν μαζί.
## Δομή της εργασίας
1. Δημιουργία MONGODB container
   * Το container έχει όνομα mongodb και ανταποκρίνεται στην port 27017 του host. 
      * Η δημιουργία του MONGODB container με όνομα mongodb πραγματοποιήθηκε με την εντολή:  `sudo docker run -d -p 27017:27017 --name mongodb mongo`
      * Με τη χρήση της εντολής: `sudo docker exec -it mongodb mongo` 
