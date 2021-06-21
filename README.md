# Ergasia2_e18012_Arvaniti_Maria
![Python](https://img.shields.io/badge/Python-v^3.8.5-blue.svg?logo=python&longCache=true&logoColor=white&colorB=5e81ac&style=flat-square&colorA=4c566a)
![Flask](https://img.shields.io/badge/Flask-v^1.1.2-blue.svg?longCache=true&logo=flask&style=flat-square&logoColor=white&colorB=5e81ac&colorA=4c566a)
![MongoDB](https://img.shields.io/badge/MongoDB-v%5E4.4-red.svg?longCache=true&style=flat-square&logo=scala&logoColor=white&colorA=4c566a&colorB=bf616a)
## Εισαγωγή
Το συγκεκριμένο project αφορά το εργαστήριο του μαθήματος «(ΨΣ-152) Πληροφοριακά Συστήματα» του τμήματος Ψηφιακών Συστημάτων του Πανεπιστημίου Πειραιώς και πραγματοποιήθηκε ως μέρος της εξαμηνιαίας εργασίας. Κάνοντας χρήση Python και Flask υλοποιήθηκε web service το οποίο παρέχει τα απαραίτητα endpoint στους χρήστες του, ώστε να μπορούν να εκτελεστούν ορισμένες λειτουργίες. Το web service συνδέεται με ένα container της MongoDB. Τέλος, το web service έγινε  containerized με χρήση Dockerfile και docker-compose ώστε το web service και η MongoDB να τρέχουν μαζί.
## Σύστημα
1. Δημιουργία MONGODB container
   * Το container έχει όνομα mongodb και ανταποκρίνεται στην port 27017 του host. 
      * Η δημιουργία του MONGODB container με όνομα mongodb πραγματοποιήθηκε με την εντολή:  `sudo docker run -d -p 27017:27017 --name mongodb mongo`
      * Με τη χρήση της εντολής: `sudo docker exec -it mongodb mongo` 
2. Δημιουργία Dockerfile
   * Υπάρχουν οι εντολές:
      * Επιλογή του base image για την νέα εικόνα που θα δημιουργήσουμε: `FROM ubuntu:latest`
      * Εκτέλεση της εντολής apt-get update μέσα στο image για να σιγουρευτούμε ότι το σύστημά μας είναι up-to-date: `RUN apt-get update` 
      * Εκτέλεση της εντολής μέσα στο image για την εγκατάσταση της python3 και του pip: `RUN apt-get install -y python3 python3-pip`
      * Εκτέλεση της εντολής μέσα στο image για την εγκατάσταση των βασικών πακέτων στα οποία στηρίζεται το application μας: `RUN pip3 install flask pymongo`
      * Εκτέλεση της εντολής δημιουργίας φακέλου production στο image: `RUN mkdir /production`
      * Αντιγραφή του app.py μέσα στο φάκελο app του image:: `COPY app.py /production/app.py`
      * Μετάβαση στο directory app: `WORKDIR /production`
      * Ορισμός του default command (Το entrypoint είναι εκτελέσιμο αρχέιο) που θα εκτελείται όταν τρέχει το container του image: `ENTRYPOINT [ "python3", "-u", "app.py" ]`
  * Για την δημιουργία του image εκτελούμε την εντολή `sudo docker build -t flask . --no-cache `
3. Δημιουργία docker-compose
   * Δημιουργία αρχείου docker-compose.yml στο οποίο υπάρχουν οι εντολές:
      * `version:2` H τρέχουσα έκδοση
      * `services: mongodb   flask-service`: Οι υπηρεσίες που θα τρέχουν μαζί
      * Στην υπηρεσία mongo υπάρχουν οι εντολές:
        * `image`: τύπος εικόνας
        * `restart: always`
        * `container-name`
        * `volumes: ./mongodb/data:/data/db`: volume σε ένα φάκελο του host που ονομάζεται data, ώστε στη περίπτωση που το container διαγραφεί, να αποφευχθεί η απώλεια των
δεδομένων
        * `ports: 27017:27017`: τρέχει στην πόρτα 27017
      * Στην υπηρεσία flask-service υπάρχουν οι εντολές:   
        * `build`: για το image flask
        * `restart: always`
        * `container-name`
        * `depends_on: mongodb`: Ξεκινάμε από το mongodb και για να προχωρήσουμε στο flask-service το σύστημα σιγουρεύεται ότι το mongodb είναι up
        * `environment: - "MONGO_HOSTNAME=mongodb"` : Εντολή που ορίζει το όνομα του host με χρήση environment variable έτσι ώστε να το γνωρίζει το flask
   * Για την δημιουργία του docker-compose εκτελούμε την εντολή (αφού έχουμε εγκαταστήσει το docker-compose)`sudo sudo docker-compose up -d` στο directory που βρίσκεται το αρχείο .yml
 4. Δημιουργία mongodb
   * Η δημιουργία του MONGODB container με όνομα mongodb πραγματοποιήθηκε με την εντολή:  `sudo docker run -d -p 27017:27017 --name mongodb mongo`
## How to run
 *  Εφόσον υπάρχει ο κώδικας στον υπολογιστή μας, δηλαδή ο φάκελος flask, ο φάκελος mongodb και το docker-compose file  εκτελούμε την εντολή (αφού έχουμε εγκαταστήσει το docker-compose)`sudo sudo docker-compose up -d` στο directory που βρίσκεται το αρχείο .yml
 *  Αφού περιμένουμε λίγη ώρα προκειμένου το Docker να κατεβάσει τα images και να δημιουργήσει τα container, είμαστε έτοιμοι να περιηγηθούμε στην εφαρμογή εκτελώντας το app.py Αρχείο και τρέχοντας τα endpoints μέσω τερματικού με τρόπο που θα περιγραφεί παρακάτω.
