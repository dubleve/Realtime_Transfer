from firebase import firebase

firebase = firebase.FirebaseApplication('https://pnu-dubleve.firebaseio.com/')


#result_get = firebase.get('/labeled_data', None)
result_put = firebase.put('labeled_data', 'test3', 'merong')
print(result_get)
print(result_put)

