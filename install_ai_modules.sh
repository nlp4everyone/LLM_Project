# Update chat model, embedding model
project_name="ModelServing"
git clone https://github.com/nlp4everyone/$project_name.git

# Copy file
rm -rf chat_modules
rm -rf embedding_modules
rm -rf config/params.py
cp -rf $project_name/chat_modules chat_modules
cp -rf $project_name/embedding_modules embedding_modules
cp -rf $project_name/config/params.py config/params.py

echo "Coping files done!"

# Install packages
#pip install -r $project_name/requirements.txt

# Remove folder
rm -rf $project_name
