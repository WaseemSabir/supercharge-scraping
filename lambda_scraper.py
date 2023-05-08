"""
This file includes the content that will be deployed to lambda function.
"""

import json
import requests as requests
from bs4 import BeautifulSoup
import boto3


def scrap_data_with_bs4(page: int):
    """
    This function scrapes the doctors data from https://www.iwantgreatcare.org/search site.
    The purpose is to collect Doctors name, speciality etc. And then for each doctor's hospital,
    the hospital's postal code is scraped from it's corresponding link.

    :param page: no of page to scrap.
    returns all doctors info on a page number.
    """
    temp = []
    url = f"https://www.iwantgreatcare.org/search?search=&near=&categories[GPs]=1&absolute=2&page={page}"
    r = requests.get(url=url)
    r.raise_for_status()

    soup = BeautifulSoup(r.content, 'html.parser')
    drs = soup.find_all("div", class_="entity")

    for dr in drs:
        text_div = dr.find(class_="doc-text")

        name = text_div.find("h5").string

        speciality = None
        speciality_div = text_div.find("span", class_="specialties")
        if speciality_div:
            inner_div = speciality_div.find("span", class_="green")
            speciality = inner_div.string if inner_div else None

        hospital_name, hospital_postcode, hospital_link = None, None, None
        locations_div = text_div.find("span", class_="locations")
        if locations_div:
            inner_div = locations_div.find("a", class_="green", href=True)
            hospital_name = inner_div.string if inner_div else None
            link = inner_div["href"]

            full_link = f"https://www.iwantgreatcare.org{link}"
            hospital_link = full_link
            try:
                r2 = requests.get(url=full_link)
                r2.raise_for_status()

                hospital_soup = BeautifulSoup(r2.content, 'html.parser')
                el = hospital_soup.find("span", itemprop="postalCode")
                hospital_postcode = el.string if el else None
            except:
                pass

        obj = {
            "full_name": name,
            "speciality": speciality,
            "hospital_name": hospital_name,
            "hsp_link": hospital_link,
            "hospital_postcode": hospital_postcode
        }
        temp.append(obj)

    return temp


def lambda_handler(event, context):
    """
    Simple Lambda Handler, that is invoked by events.
    """
    page_no = event["page"]
    data = scrap_data_with_bs4(page_no)

    d = {
        "page": page_no,
        "data": data
    }

    # Store the scraped data into S3 Bucket. In your case, it can be a database or anything else.
    bucket_name = "< Bucket Name Here >"
    file_name = f"p_{page_no}.json"
    s3_path = "output2/" + file_name

    s3 = boto3.resource("s3")
    s3.Bucket(bucket_name).put_object(Key=s3_path, Body=json.dumps(d))

    # Update the current function's Configuration, each update will redeploy the lambda function.
    # which will change its IP address. This can help us bypass Rate limiting to an extent.
    lam = boto3.client('lambda')
    lam.update_function_configuration(FunctionName="scraper", Environment={
        'Variables': {}
    })

    return {
        'statusCode': 200,
        'body': json.dumps('file is created in:' + s3_path)
    }
