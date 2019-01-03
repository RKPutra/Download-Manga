import scrapy
import requests
import re
import os

class MangaSpider(scrapy.Spider):
    name = "manga"
    
    start_urls = []
    print()
    
    print("##  ##  ##   ######   ##       #####    #####    ##########   ######")
    print("##  ##  ##   ##       ##      ##       ##   ##   ##  ##  ##   ##    ")
    print("##  ##  ##   ######   ##      ##       ##   ##   ##  ##  ##   ######")
    print("##  ##  ##   ##       ##      ##       ##   ##   ##  ##  ##   ##    ")
    print("##########   ######   ######   #####    #####    ##  ##  ##   ######")
    print("====================================================================")
    print("Input a chapter link from www.readmng.com any manga you want!!!!")
    print("Note: Make sure you use vpn to avoid getting blocked\n\n")
    print("======================================")
    inp = input("link : ")
    start_urls.append(inp)
    print("======================================")
    print()

    def parse(self, response):
        JUDUL_SELECTOR = 'title ::text'
        raw_judul = response.css(JUDUL_SELECTOR).extract_first()
        t = raw_judul.split()
        indek = 0
        for i in range(len(t)):
            if t[i] == "-":
                break
            indek += 1
        print()
        judul = ' '.join(t[0:indek])

        try:
            os.makedirs(judul)
        except OSError:
            pass
        os.chdir(judul)
        
        IMAGE_SELECTOR = '#chapter_img ::attr(src)'

        image_url = response.css(IMAGE_SELECTOR).extract_first()
        raw_filename = image_url.split('/')[-1]
        filename_indek = 0
        for i in range(len(raw_filename)):
            if raw_filename[i] == "?":
                break
            filename_indek += 1
        filename = raw_filename[:filename_indek]
        img_data = requests.get(image_url).content

        with open(filename, 'wb') as handler:
            handler.write(img_data)

        os.chdir("../")

        NEXT_PAGE_SELECTOR = '.chapter_next_page ::attr(href)'
        next_page = response.css(NEXT_PAGE_SELECTOR).extract_first()
        if next_page:
            yield scrapy.Request(
                response.urljoin(next_page),
                callback=self.parse
            ) 