import asyncio
import httpx
import aiohttp
import time
from random import randint
from flask import Flask, render_template, request
from flask_restx import Api, Resource

app = Flask(__name__)
api = Api(app)

# function converted to coroutine
async def get_xkcd_image(session):
    random = randint(0, 300)
    result = await session.get(f'http://xkcd.com/{random}/info.0.json') # dont wait for the response of API
    return result.json()['img']

# function converted to coroutine
async def get_multiple_images(number):
    async with httpx.AsyncClient() as session: # async client used for async functions
        tasks = [get_xkcd_image(session) for _ in range(number)]
        result = await asyncio.gather(*tasks, return_exceptions=True) # gather used to collect all coroutines and run them using loop and get the ordered response
    return result


@app.route('/comic')
class Comic(Resource):
  async def get(self):
      start = time.perf_counter()
      urls = await get_multiple_images(5)
      end = time.perf_counter()
      markup = f"Time taken: {end-start}<br><br>"
      for url in urls:
          markup += f'<img src="{url}"></img><br><br>'

      return markup

async def get_book_name2(index: int, isbn: int) -> str:
    async with httpx.AsyncClient() as client:
        response = await client.get(f"https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn}")
        response_dict = response.json()
        # print(response_dict)
        if response_dict["totalItems"] == 1:
          title = response_dict["items"][0]["volumeInfo"]["title"]
          print(f"{isbn} : {index}: {title} ")
          return "\{'isbn' : {isbn}, 'index' : {index}, 'title': {title}\}"
        else:
          print(f"{isbn} : {index}:  nil")
          return "\{'isbn' : {isbn}, 'index' : {index}, 'title': ''\}"

async def get_book_name(index: int, isbn: int):
    print(f"get_book_name......... aiohttp ")
    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn}") as response:
            response_dict = await response.json()
            
            if response_dict["totalItems"] == 1:
                title = response_dict["items"][0]["volumeInfo"]["title"]
                print(f"{isbn} : {index}: {title} ")
                return {'isbn': isbn, 'index': index, 'title': title}
            else:
                print(f"{isbn} : {index}:  nil")
                return {'isbn': isbn, 'index': index, 'title': ''}


async def async_test():
    isbn_list = [
        9780007355143,
        9780008108298,
        9780547249643,
        9781405882583,
        9780316095860,
        9780930289232,
        9780486415871,
        9780765350381,
        9781716814655,
        9789898559425,
        9781944529024,
        9780765376671,
        9781400079988,
        9781438114026,
        9780393066258
    ]
    
    task_list = []
    for index, isbn in enumerate(isbn_list):
        task_list.append(get_book_name(index, isbn))
    out = await asyncio.gather(*task_list)

    return out

@api.route('/hello/<string:name>')
class HelloWorld(Resource):
  def get(self, name):
    # asyncio.run(async_test())
    # print(f"Inside flask function: {threading.current_thread().name}")
    start = time.perf_counter()
    # asyncio.set_event_loop(asyncio.new_event_loop())
    # loop = asyncio.get_event_loop()
    # result = loop.run_until_complete(async_test())
    result = asyncio.run(async_test())
    
    print("RESULT : %s " % result)
    # return jsonify({"result": result})
    end = time.perf_counter()
    aa = (end - start)
    print(f"message : Welcome, {name} start {start} - end {end}  {aa}!")
    # return {"message" : "Welcome, %s start %s - end %s  %s!" % (name, start, end, (end-start))}
    return result
    
@app.route('/async', methods=['GET', 'POST'])
async def async_form():
  async with httpx.AsyncClient() as client:
    googleResponse, naverResponse, daumResponse = await asyncio.gather(
        client.get(f'https://www.google.com', timeout=None),
        client.get(f'https://www.naver.com'),
        client.post(f'https://www.daum.net')
    )

  resp = {
            "google_response" : googleResponse,
            "naver_response": naverResponse,
            "daum_response" : daumResponse
  }
  print(resp)
  
  return "OK"


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=9999)