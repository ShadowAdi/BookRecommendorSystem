from flask import Flask,render_template,request
import pickle
import numpy as np

app=Flask(__name__)
popularDF=pickle.load(open("popular.pkl","rb"))
pt=pickle.load(open("pivot.pkl","rb"))
books=pickle.load(open("books.pkl","rb"))
similarity_scores=pickle.load(open("Similarity.pkl","rb"))
rounded_data = [round(value, 2) for value in popularDF["Avg_Rating"].values]
shortened_data = [item[:35] for item in popularDF["Book-Title"].values]  # Take only the first 10 characters of each string




@app.route("/")
def index():
    return render_template("index.html",
                           book_name=list(shortened_data),
                           images=list(popularDF["Image-URL-M"].values),
                           author=list(popularDF["Book-Author"].values),
                            votes=list(rounded_data),
                            rating=list(popularDF["Rating"].values)
                           )


@app.route("/Recommend")
def recommendUi():
    return render_template("Recommendation.html")


@app.route("/recommendation",methods=["POST"])
def recommend():
   user_Input = request.form.get("userInput")
   index_array = np.where(pt.index == user_Input)[0]
   
   if index_array.size > 0:
        index = index_array[0]
        similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:6]

        data = []
        for i in similar_items:
            item = []
            temp_df = books[books["Book-Title"] == pt.index[i[0]]]
            item.extend(list(temp_df.drop_duplicates("Book-Title")["Book-Title"].values))
            item.extend(list(temp_df.drop_duplicates("Book-Title")["Book-Author"].values))
            image_list = list(temp_df.drop_duplicates("Book-Title")["Image-URL-M"].values)
            updated_url_list = [url.replace("http://", "https://") for url in image_list]
            item.extend(updated_url_list)
            data.append(item)

        if len(data) > 0:
            return render_template("Recommendation.html", data=data)
        else:
            message = "No Image For Such Name Is Found"
            return render_template("Recommendation.html", message=message)
   else:
        message = "No Book Found for the given input"
        return render_template("Recommendation.html", message=message)







if __name__=="__main__":
    app.run(debug=True)