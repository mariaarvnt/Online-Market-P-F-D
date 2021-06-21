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
## Υλοποίηση ζητούμενων endpoints
   0. Πριν την υλοποίηση των endpoints προηγήθηκε η σύνδεση με την mongodb, η δημιουργία των Collections Users, Products
 *USERS*: To collection αυτό περιέχει εγγραφές χρηστών του συστήματος. Κάθε χρήστης έχει name: Ονοματεπώνυμο, e-mail: e-mail, password: Το password, category: Κατηγορία χρήστη (με τιμή user ή admin), orderHistory: Το ιστορικό των παραγγελιών του χρήστη (μόνο για τη περίπτωση user και όχι admin), cart: το καλάθι του χρήστη (μόνο για τη περίπτωση user και όχι admin)
 *PRODUCTS*: To collection αυτό περιέχει εγγραφές προϊόντων του συστήματος. Κάθε προϊόν έχει p_name: Όνομα, p_category: Κατηγορία, stock: Απόθεμα, descr: Περιγραφή, price:Τιμή
 * Για τον απλό χρήστη: 
   1. **_createUser_** : Δημιουργία user ο οποίος θα εισάγεται στο collection Users και θα έχει μοναδικό email και password
        * Πραγματοποιείται post request- μέθοδος από τον χρήστη η οποία ονομάζεται create_user με την εντολή `def create_user()` εντός της οποίας αρχικά φορτώνονται τα δεδομένα που δίνει ο χρήστης με την εντολή `data = json.loads(request.data)` και ένα exception handling σε περίπτωση που ο χρήστης έχει δώσει ελειπή ή λάθος στοιχεία.
        * Έχουμε πρόσβαση στο συγκεκριμένο method με την χρήση της εντολής `curl http://localhost:5000/createUser -d '{"email":"da@gmail.com", "name":"Dimitra Anagnostopoulou", "password":"kgljrjgo5dg"}' -H "Content-Type: application/json" -X POST`. Τα da@gmail.com, Dimitra Anagnostopoulou, kgljrjgo5dg είναι παραδείγματα email, name και password αντίστοιχα.
        * Με την επιτυχή φόρτωση των δεδομένων, ελέγχουμε αν υπάρχει ήδη κάποιος χρήστης με το ίδιο username που δώσαμε με την εντολή ` users.count_documents({"email":data["email"]}) ` η οποία κάνοντας χρήση της count_documents() μετρά τις εγγραφές που έχουν αυτό το email. Έτσι:
            * `if users.count_documents({"email":data["email"]})== 0 :`, δηλαδή αν δεν υπάρχει ήδη κάποιος χρήστης με αυτό το email γίνεται εισαγωγή του χρήστη με τα στοιχεία του στο collection users με τις εντολές `user = {"email": data['email'], "name": data['name'], "password": data['password'], "category":"user"}` `users.insert_one(user)` ενώ επιστρέφεται μήνυμα επιτυχίας με την εντολή  `return Response("User with email " + data['email'] + " was added to the MongoDB", status=200, mimetype='application/json')"`
            * Το αποτέλεσμα στο τερματικό της επιτυχούς προσθήκης ενός νέου χρήστη είναι `User with email da@gmail.com was added to the MongoDB`, ενώ στο mongoshell με χρήση των εντολών `use DSMarkets` `db.Users.find({"email": "da@gmail.com"})` είναι `{ "_id" : ObjectId("60d0517e84ab38a0dcdbe7df"), "email" : "da@gmail.com", "name" : "Dimitra Anagnostopoulou", "password" : "kgljrjgo5dg", "category" : "user", "cart" : [ ] }`
            * `else` , δηλαδή αν υπάρχει ήδη κάποιος χρήστης με αυτό το email επιστρέφεται μήνυμα λάθους με την εντολή `return Response("A user with the given email already exists", status=400, mimetype='application/json')` και άρα εμφανίζεται στο τερματικό `A user with the given email already exists` 
   2. **_login_** : Σύνδεση χρήστη με τα προσωπικά email και password που εισήγαγε προηγουμένως
        * Πραγματοποιείται post request- μέθοδος από τον χρήστη η οποία ονομάζεται login με την εντολή `def login()` εντός της οποίας αρχικά φορτώνονται τα δεδομένα που δίνει ο χρήστης με την εντολή `data = json.loads(request.data)` και ένα exception handling σε περίπτωση που ο χρήστης έχει δώσει ελειπή ή λάθος στοιχεία.
        * Έχουμε πρόσβαση στο συγκεκριμένο endpoint με την χρήση της εντολής `curl http://localhost:5000/login -d '{"email":"da@gmail.com", "password":"kgljrjgo5dg"}' -H "Content-Type: application/json" -X POST`. Τα da@gmail.com, kgljrjgo5dg είναι παραδείγματα email και password αντίστοιχα. 
        * Με την επιτυχή φόρτωση των δεδομένων, πραγματοποιείται προσπάθεια αυθεντικοποίσης του χρήστη με την εντολή `user_found = users.find_one({"email":data["email"], "password":data["password"]})` στην οποία δημιουργούμε και εκχωρούμε στην μεταβλητή `user_found` το αποτέλεσμα της εύρεσης του email και password στα δεδομένα  `data["email"] == user_found["email"] and data["password"] == user_found ["password"]`. Σε περίπτωση που το username και password που υπάρχει στην βάση ταυτίζεται με το username που έδωσε ο χρήστης, δηλαδή `if (data["email"] == user_found["email"] and data["password"] == user_found ["password"]):`, έχουμε:
            * `user_uuid = create_session(user_found["email"])` , δηλαδή κλήση της υλοποιημένης συνάρτησης create_session()- η οποία επιστρέφει ένα string uuid όταν κάποιος χρήστης συνδέεται- με παράμετρο το `user_found["email"]` δηλαδή το email του χρήσττη στην βάση το οποίο εκχωρείται σε μία μεταβλητή που ονομάζεται user_uuid
            * `res = {"uuid": user_uuid, "email": data['email']}`, δηλαδή δημιουργούμε ένα dictionary με όνομα res το οποίο θα περιέχει αυτό το user_uuid - διαφορετικό σε κάθε σύνδεση και το email του χρήστη
            * Τέλος, επιστρέφονται τα user_uuid, password και μήνυμα επιτυχίας με την εντολή  `return Response(json.dumps(res), status=200, mimetype='application/json'))` (Έχει εισαχθεί status code 200)
            * Αποτέλεσμα: `{"uuid": ["ee6636ec-d26d-11eb-84a9-e90961b205b2", "839c40bf-6c63-4150-bc03-533e6d82dd17"], "email": "da@gmail.com"}`
         * Σε περίπτωση που δεν υπάρχει στην βάση το username που έδωσε ο χρήστης ή ο κωδικός του είναι λανθασμένος και η αυθεντικοποίηση δεν είναι επιτυχής:
            * Επιστρέφεται μήνυμα λάθους με την εντολή `return Response('No user found with given email or password', status=400, mimetype='application/json')`, δηλαδή αποτέλεσμα: `No user found with given email or password`   
   3. **_searchByName_** : Αναζήτηση προϊόντος βάσει ονόματος
        * Πραγματοποιείται get request- μέθοδος από τον χρήστη η οποία ονομάζεται search_by_name με την εντολή `def search_by_name()` εντός της οποίας αρχικά φορτώνονται τα δεδομένα που δίνει ο χρήστης με την εντολή `data = json.loads(request.data)` και ένα exception handling σε περίπτωση που ο χρήστης έχει δώσει ελειπή ή λάθος στοιχεία.
        * Έχουμε πρόσβαση στο συγκεκριμένο endpoint με την χρήση της εντολής `curl -H "Authorization: cbee9892-cc38-11eb-a024-9d77b2d852ab" http://localhost:5000/searchByName -d '{"email": "da@gmail.com", "password":"kgljrjgo5dg","p_name":"500"}' -H "Content-Type: application/json" -X GET`. Τα ee6636ec-d26d-11eb-84a9-e90961b205b2, da@gmail.com, kgljrjgo5dg, 500 είναι παραδείγματα uuid, email, password, p_name αντίστοιχα.   
        * Με την επιτυχή φόρτωση των δεδομένων του αρχείου, με την εντολή `uuid = request.headers.get('authorization')` ο χρήστης περνάει το uuid το οποίο έχει λάβει κατά την είσοδό του στο σύστημα έτσι ώστε να αυθεντικοποιηθεί. Για τον έλεγχο του uuid κλήθηκε η συνάρτηση is_session_valid() με παράμετρο το uuid - η οποία επιστρέφει true εάν το uuid βρεθεί εντός των users_sessions). Σε περίπτωση που υπάρχει uuid ανάμεσα στα users_sessions, δηλαδή `if is_session_valid(uuid)`, έχουμε:
            * Επιτυχή αυθεντικοποίηση του χρήστη 
            * Αναζήτηση στα δεδομένα το δοθέν από τον χρήστη email και εκχώρηση αυτού στην μεταβλητή user_session με την εντολή `user_session = users.find_one({"email":data["email"]})` . Χρησιμοποιήθηκε η method find_one() έτσι ώστε να βρούμε τον (πρώτο) χρήστη με αυτό το email. Στην περίπτωση που υπάρχει αυτός ο φοιτητής, δηλαδή `if user_session`:     
              * Απαιτείται να ελέγξουμε την κατηγορία του αφού μόνο οι users μπορούν να αναζητήσουν προϊόντα.Άρα με τον έλεγχο `if user_session["category"] == "user":`           ελέγχεται ο συγκεκριμένος χρήστης (τον οποίο ταυτοποιήσαμε στο προηγούμενο βήμα) εάν η κατηγορία του είναι user. Στην περίπτωση που είναι:
                * Δημιουργία λίστας που θα αποθηκεύσει τα προϊόντα- αποτελέσματα της αναζήτησης με την εντολή `products_list = []`
                * Εύρεση προϊόντων που έχουν στο όνομά τους (p_name) το όνομα που εισήγαγε στην αναζήτησή του ο χρήστης και εισαγωγή τους στην λίστα `same_products` με την εντολή `same_products = list(products.find({"p_name" : {"$regex" : data['p_name']}}))`. Εδώ χρησιμοποιήθηκε ο τελεστής `$regex` που βοηθά στην εύρεση όσων εγγραφών περιέχουν το pattern που δόθηκε μέσω του data['p_name']. 
                  * Αν δεν βρεθούν προϊόντα που ταιρίαζουν στα κριτήτια αναζήτησης, δηλαδή `if len(same_products) == 0:`, τότε επιστρέφεται μήνυμα αποτυχίας `return Response("No products found with the name " + data['p_name'], status=500, mimetype="application/json")`
                  * Για τα προϊόντα που θα βρεθουν `for product in same_products:`, θα εισαχθούν στην λίστα `products_list` με την εντολή `products_list.append(product)` αφού πρώτα μετατραπεί σε string το _ id - μοναδικό αναγνωριστικό που προσθέτει η βάση σε κάθε αντικείμενο και είναι τύπου ObjectId. Η μετατροπή θα γίνει με την εντολή   `product['_id'] = str(product['_id'])`
                  * Τέλος, η λίστα θα ταξινομηθεί βάσει των ονομάτων των προϊόντων σε αλφαβητική σειρά με την μέθοδο `sorted()` και την `lambda function` ως εξής `products_sorted_list = sorted(products_list,  key=lambda products: data['p_name'])`
                  * Επιστρέφεται η λίστα `return Response(json.dumps(products_sorted_list, indent=2), status=200, mimetype='application/json')` ως απάντηση. Στο παράδειγμά μας θα επιστρεφόταν `[
  {
    "_id": "60c71f549d6daceffd4550f5",
    "p_name": "Antibacterial Lavender Cream Soap Spare 500ml",
    "p_category": "Personal Care Items",
    "stock": 100,
    "descr": "Dettol Liquid Cream Soap provides your skin with a gentle antibacterial protection against microorganisms. Its unique composition for sensitive skin leaves your hands with a feeling of softness and hydration. It is important to wash your hands thoroughly daily. Use Dettol Moisturizing Cream Soap and let your hands feel hydrated and clean. With a pleasant lavender scent.",
    "price": 2.55
  },
  {
    "_id": "60c720c89d6daceffd4550f7",
    "p_name": "Spaghetti No7 500g",
    "p_category": "Basic standard foods",
    "stock": 400,
    "descr": "Spaghetti No7 Melissa is a classic pasta of fine Greek grains with golden color and authentic taste. A thin pasta that is extremely versatile as a base for everyday cooking, but can also be used in more gourmet recipes. It is cooked plain, with cheese, with red or white sauces. It goes perfectly with Greek classic recipes such as spaghetti with minced meat, but also with modern recipes.",
    "price": 0.97
  }
] `, δηλαδή τα δύο προϊόντα που έχουν στο όνομά τους το '500'. 
              * Σε περίπτωση που το email δεν ανήκει σε user αλλά σε admin επιστρέφεται το μήνυμα `Only users can perform this operation`
            * Σε περίπτωση που το email που δίνεται δεν αντιστοιχεί σε κάποιο χρήστη επιστρέφεται το μήνυμα `No user found with given email`
        * Εάν το uuid είναι λανθασμένο για το συγκεκριμένο session επιστρέφεται το μήνυμα `User not Authenticated`
   4. **_searchByCategory_** : Αναζήτηση προϊόντος βάσει ονόματος        
