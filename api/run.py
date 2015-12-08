#!flask/bin/python
# from app import app
# app.run(debug=True)
import os
os.environ["AWS_ACCESS_KEY_ID"] = 'AKIAJCSJR3BZJ62BMDVQ'
os.environ["AWS_SECRET_ACCESS_KEY"] = '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'

from app import app



port = int(os.environ.get('PORT', 5000))

# Use this if you wanna run the script on Heruku server
app.run(host='0.0.0.0', port=port, debug=True)

# Uncomment this if you wanna run the script locally
# app.run(debug=True)