# Flask API med members database

Punkt 1-9 i øvelsen er alle lavet, mens jeg har været ved at fange eventuelle fejl og give de rigtige beskeder og response status codes, når en fejl opstår. Har dog ikke fået tjekket for alle fejl eller om exceptions og errors bliver returneret korrekt.

## Routes
```python
# SAME AS /members
@app.route('/', methods=['GET'])

# RESET DATABASE AND GET 10 RANDOM MEMBERS
@app.route('/reset', methods=['GET'])


# --- MEMEBERS
# GET ALL MEMBERS
@app.route('/members', methods=['GET'])

# POST NEW MEMBER
@app.route('/members', methods=['POST'])

# PUT MEMBER (REPLACE/UPDATE DATA)
@app.route('/members/<int:member_id>', methods=['PUT'])

# PATCH MEMBER (UPDATE PART OF THE DATA)
@app.route('/members/<int:member_id>', methods=['PATCH'])

# DELETE MEMBER BY ID
@app.route('/members/<int:member_id>', methods=['DELETE'])

# GET MEMBER BY ID
@app.route('/members/<int:member_id>', methods=['GET'])


# --- GITHUB API
@app.route('/api/members/<int:member_id>', methods=['GET'])
```
