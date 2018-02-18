import requests 
from bs4 import BeautifulSoup
import pandas as pd

data={
'__EVENTTARGET':'',
'__EVENTARGUMENT':'',
'__VIEWSTATE':'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',
'__VIEWSTATEGENERATOR':'F8CFDE04',
'__EVENTVALIDATION':'2F6jAY9uzBTR40IbkeQyy655o+9U3PVs6MRatJpFaLT7yVIeZPMNTpcct235LC8XXiYlWOvw1bZlgVtk2JUnBuhi24Y16cc7hOuljjrA9RxpVWAeo3BGEuUSyJamU8XcgMVmk045521Y5ZR85zU5leaXv23C33WMp7Zg5HDU/VOxR1nnBTClhJh5GzJhZ1Kr3yCyabFDqoNzIOhrM1RbUi5s4BLq2gdlUxnx8acypdHrSNfU8oTZEbR1Nc0kyt/XJsYOxOZJwJ1UyuEkq2fag3DYSyZcgWT/IFuHadj5wf8SbSPpa981lwfHPRDzNJma2YdwRkPOkfS/O1Hz9NQk3C/SvlPXG9qWD6MwLsskh+sgU8GNWwizgny/ENib88WcDVsSslQmpyeCGF2AZqcPQGhjy9Hm35U5LlHeYN0h/KT87druuUARjH/6J6g2BU0ERJop+s/JPg2nrYTDAkTq/DieuDMf97t4/qnXMcooTVo4YWn91V+AT1p3pO+L7faumwAI+ejDwpXh86srLbCqdC+zjaHA/0OddTgmCIB9hIUJBMe5YZkQZ0QfrhotWe5QLAyxt0xmczC7RiA/TYPqLPJMQXj54aFmzH6EBRtvjd8mf7r0/N5QHFVLGf5j94GIOWubVLb6ZEZjtABhhfkds+3WD9q+2TWMUjbkPoOiyirWb5w/8BjWqnjM8pc+3XipYy9xEnUh/o5QYujKQPCfi49g1L1vGB1V1hrOjFWGNwqQIfaOwqaEExuswRLa93xSjxJexVSZKTApZmMqTOlPZXoG64RJIGY81+ubbPfNHQCBMNJv2MJbInW80riboJDN4Mr8RBLDZKMTw8ED4Qx69z0t/hCotnE6XK9io7nXkxsJ690HnwoiPNQA6jBqRW4Y5WDfHDuWZhi4Eh8izS1viSHLtkwyVrVGlEOZJrqWPzKHPdgXI5tF6NKZdDisV8AHabjV/N7gEIDrhYIg9r7QXP7uhkMMfAz9b3jDWiCH/5SDKtZn27udiia++or0cxIvFcAHy8MzIJb1CHDj2juh+3udRV0MXqRezdD+D/iXMbltRr9uMzbMdXcDpvdW453iTHaIof4325WCnpkNXeOmTo6th3a0rdSPENdPNm2RJnH8dY5nstATOUSuy4A/a9Lx+ayYZud5CyG1oo0dhTMGWs15drrHWgE4+G44+ElwJg1z/HS2qGRYBVdvJcdpWIYkfYJ8FA==',
'ctl00$tbCompanySearch':'',
'ctl00$MainContent$sfMessageType$txtObjectName':'Сообщение о выпуске независимой гарантии',
'ctl00$MainContent$sfMessageType$hfIdObject':'IssueIndependentGuarantee',
'ctl00$MainContent$sfMessageType$hfAdditionalInfo':'',
'ctl00$MainContent$cbShowForeignSystemMessages':'on',
'ctl00$MainContent$sfCompanySelector$txtObjectName':'',
'ctl00$MainContent$sfCompanySelector$hfIdObject':'',
'ctl00$MainContent$sfCompanySelector$hfAdditionalInfo':'',
'ctl00$MainContent$sfIndividualEntrepreneur$txtObjectName':'',
'ctl00$MainContent$sfIndividualEntrepreneur$hfIdObject':'',
'ctl00$MainContent$sfIndividualEntrepreneur$hfAdditionalInfo':'',
'ctl00$MainContent$sfAppraiser$txtObjectName':'',
'ctl00$MainContent$sfAppraiser$hfIdObject':'',
'ctl00$MainContent$sfAppraiser$hfAdditionalInfo':'',
'ctl00$MainContent$sfPerson$txtObjectName':'',
'ctl00$MainContent$sfPerson$hfIdObject':'',
'ctl00$MainContent$sfPerson$hfAdditionalInfo':'',
'ctl00$MainContent$sfNonResidentCompany$txtObjectName':'',
'ctl00$MainContent$sfNonResidentCompany$hfIdObject':'',
'ctl00$MainContent$sfNonResidentCompany$hfAdditionalInfo':'',
'ctl00$MainContent$dpBeginPublishDate$txtDate':'01.01.2018',
'ctl00$MainContent$dpEndPublishDate$txtDate':'',
'ctl00$MainContent$tbMessageNumber':'',
'ctl00$MainContent$btnSearch':'Поиск',
'ctl00$MainContent$ucMonitoringControl$txtEmail':'',
'ctl00$MainContent$ucMonitoringControl$txtPassword':''}

head1={
'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
'Accept-Encoding':'gzip, deflate, br',
'Accept-Language':'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
'Cache-Control':'max-age=0',
'Connection':'keep-alive',
'Content-Length':'13104',
'Content-Type':'application/x-www-form-urlencoded',
'Host':'se.fedresurs.ru',
'Origin':'https://se.fedresurs.ru',
'Referer':'https://se.fedresurs.ru/Messages',
'Upgrade-Insecure-Requests':'1',
'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.167 Safari/537.36'}

head2={
'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
'Accept-Encoding':'gzip, deflate, br',
'Accept-Language':'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
'Cache-Control':'max-age=0',
'Connection':'keep-alive',
'Host':'se.fedresurs.ru',
'Referer':'https://se.fedresurs.ru/Messages',
'Upgrade-Insecure-Requests':'1',
'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.167 Safari/537.36'}

msg_head={
'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
'Accept-Encoding':'gzip, deflate, br',
'Accept-Language':'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
'Connection':'keep-alive',
'Host':'se.fedresurs.ru',
'Referer':'https://se.fedresurs.ru/messages/IsSearching',
'Upgrade-Insecure-Requests':'1',
'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.167 Safari/537.36'}


url1='https://se.fedresurs.ru/Messages'
url2='https://se.fedresurs.ru/messages/IsSearching'
#data='__EVENTTARGET=&__EVENTARGUMENT=&__VIEWSTATE=ki33%2FCvKVXjBPKZpSML3Hn%2FyNt7dwjtHh6lP%2F%2BBh2MgKSv4y9qrPVmlfbmlNRXzqudFDJ0xY9zDeNTnCzJD4Ur6pvdVXbvpUmp%2FR3j08hVVvyQkjFWrbw5s%2BtrHdZbGMurCWva9GRfcmlv2JcxQ5uzOMMEtaQ6Rg1td2lOwmFaeB9cKBDBgXonjhvjbTkUd7Z8TsR18r6jOXgNgvsXa73WAkIdUzqFVh4aS2V%2FRYCDYo5ZnBMQFxOdd9ddk5GoZ5N7V%2BFODlhcJDZIuXZTSzdzk3J9SYJfQptF0NkI63%2Fvu5wxAIF%2FR3ihe8yBxg%2BW5w9YS7emDaUPUqSzoyR21QenOBMhiJq3CoNLtSMMmZRLrmYTjeHqe9oiuoS5eIaHI%2FtdFDoU891PQYzDGyOYTXNWW4s%2FcLRM1HKQNyZVhDan6ERRtrwbuQHsqhOLUVvEMnMW%2BxMinFokH0jWYkta3qInylk7Z%2F4pDDVRHo06srB1ochxAW9bgmvYkKYroIFj%2BUH5NdJhPQwJY72FeeVrzQD63ggEq7C4%2Ba5Ctabn3h%2FKtt9Hh41x9%2FgUmCB35MayOHZshwYtefDyNkF0FdyRu1Pz35k57ARr2nXBf7q5PPGZLF%2BlV8pNRSc9R9VXKaR0Hb4wV6CKFY0hIOXJgZlzBM%2BQUY4C5f2%2BNgQ1CqrmFs0C37USxquCYv7DnCjyvUbeknbMN8NauX1hoUcECOuMjy4ii%2Flmap19jumjnxgAEaf8RqK6LdbZxp%2FWSNvSfv0a%2FNi8mqTFGULPPAPoSIDmYDrW5sjF%2FGglAT%2BhvkhTDNYt%2BHNz62LVRI1aoh79Jdsl2O04Mo6o%2FffyK7D%2B%2B4hqRXE40VqEV%2FluGvUcWIhM5ksza5TFUYA9EyCbFU4CJup5vKxkQYtI5tlY211cpa6gTsB2BTxj8btc4sz%2BewSYgk8wZJOzEFDXX2ttMjw%2FGFZ9gWfwp%2FJxbTuTZqiJR95ni3NrMA29S72gY9cX3PXJJqd3BLU%2FHYquk2i8JBkb0pqZbfUocLdZNjRxq5y4%2FF9%2B3OSrFD%2BhDTHaaVSNGo5Egfj8diAOmGt9Rt9qgauM7XwnwCeVR%2BmIH1mQNS%2FNSxTVPIOvLesIJpSJcjPXkJMNfK7bHRjHGBce2sQTaMhi6dcBL3eSCZdx2u5xOGtXSuLCQxYBBugIbD8wFlijzFZQVlXN3uwITecYqafpQgxpX9EXojhKUZjzbUtEfRPqmXnZ0urXQsk52B3qBF%2FmrNd9PavozyXdkrYHFm6IsyP2404QaGR9NPJX6e3YvcgFa%2BdEsmdmKNNIiw3aJcDhEp0RNV1QkqR5hx1WA4q79XY1cZkbTX8yi%2F3pxIynYerQsgRTgFk4pJYWMpKjxIT%2BQAVB3HP4yoIGDY%2FZGEFHrh%2BilXrl8M8lOiakuVd3x6uFzJV5FHBA3SsM9xdaByMm4LhGwZ23wSRqyfTXIMsus%2BlAOOQZYYm7Tg%2B%2Fy1gSjUJTCTdxA3IgXfR3RzHCR%2B3nvb3oElNQ%2B7jVmkS4QjHllD8TpK%2F4N2fNm42hQMPs0VgptTaHTvZnoJHCAzgeUGL2X8AYisDH7xO2Qp2YEXo40DnoQMDPD7FVQWQoTzoCy3gTib46CDB3%2F%2FLG%2FG6QR65LAq1fJJ3BqHodaVqOV0NwENnVkizwVEOvsWn6RmXBZotH1k9nsXa28Dq2eAC8%2B%2B5qpghMpUvFipmPt1SC14a1JF7l2P9YJAZL3JTV2kZqdLFuG%2B4ZZZ7Py1s3BxqOrbwOXoHk0%2F977BLi7DUCSKCDF71dxD9M13BLRta%2FAReJlsf1O0gSpLl5HN%2Fj6RQ%2BbjEjHfXnD5VT%2BHWtNzPsCpofgg28mFYYMbx0BBuZyJjVjFbUDyu3zu8D0ykNN%2Bv%2BvHEs1z6E1Yy1%2FJTzIPE6JnheB761zh4Cz0gzKbqIAPqYEy4Rdp1mM7wejtUdcK%2Fp%2Fo7ZirzxhgJISfj4wsu0WQlmOOrrNqUmCwPv5jJS1KxYyPJ9EDaZ%2FINH77PT%2BsOMmSdddHYw2YvP1VF6OBvAcczP9vuY%2BX1m0CkV1TqjAXs5VRlqjDFbu52gOMTBMDIUGtL%2F93NVIkPqsrBqGN2AJfAmFmT5VEiAy6N%2BAuTh%2BflqNiufR%2BSR6%2Fk2xiO%2FcFWU4ibvnREgj2wcPaa6tuj9Zb01JpJ6ZreOuqzvQ7Gn7LMARyRgvyMMB9wgDvpX89qoSo7lRYpPvqPadlmZ5wObcBBlqFEVbe93jyhm6wa2LsiT7irUswC57rFFWiSrt5bas%2BETeC6dgdq1UO2OTAtHPbQHdPZddd5Qnrdl0xAJ2OH%2Bg2Qh%2FRR3C2Ge0Uezm7wmN6hIqUqkF5zQ%2BnlEG7zBngANdj5SOr6cj3HxS9ewJmq2BFgL0NmaPNocz3uDRvEBN1alYLcMbSFpqi4ShpXj%2FdCcq8OZ5h6LyqPxBOO2yiJTCLZ%2BDAnGBKEb5JNzseEk5c1TCrYhrbmXMo6D1fsrbg9lA2mUT9DVUVPj6Sga3oLgvu8O3VOL%2BX5VgR3ifM%2FlNGB03akW5mZQizeDrL58%2BB%2Fw0vCUoLfDz6SOfWrj3KWEeIx5akIflbxII%2Fpd1XGsY94pCgW2r2LWWdvT72kyD5P1TiiLGFGIXQoSEFta1qSRfY6Qn5Meh6OYP8W7%2Fm2ZtywwNCj8qV7RuusjG3ehSVevz8mKYuVRBwM7JlZXr2%2BaLuB4xkgkYo8dM2sDDgKulJtdt5mxX6W14UNNLsPWgwFc9gXZsfzLld%2FDE6nbaZ5Hgbu4UZAO6zFcUMHyswluAs45pFRHjMyep8G9K0aV6oyghnSeneoSx3zPaDDSWKHTDSqd6lGY3iwzUZWhpGcco9kERkS4Qpc%2Fy0FY0vBbA%2BkEH05J1AKUDPNH8SOEN8tNwZJ4LkteZ4CI8aIYtJst08HAma8Acfx584eo%2FVwhQCXVOmAu2F3A2UOirkKUSVgtWS6It%2BBJ%2F%2F7tLVaajZJlZN7HtZL%2Fqmcc3CNLP5EHtu1HvS1YWLSfllnugnFq%2Frc8s%2BqRZ04blTcuIB1f%2FWkX%2FCmvrGIlLlw9HQWF49D1LyqUGcQ53q9%2BaCYGVkKXqXzRUmKI6%2BZK%2BRG%2FiwPvwJDrpqP0AM7siz%2BP6BeOQTGkQsvQ3OObnQP%2BXXEi%2FAUzabQ2kJgaWA6NP0oZyntCMMwrG7XL8EEix99%2BuAWlcIT5NbTVkuJZQ1dPNcUbboMUjIOnObb5iESfEOEWKnMDnqtyrW3ILhYO6MYKR%2FlFbOc3byBf4WQGV3WZqU9apYNvHfTHvF%2FuPbNxnvRWcaPjh4%2B19fZiNh7H%2BaYzRoQ18Ks7OWluHMhZUDuuIhLkb6niDJ74RvMNpysDCw8IQCf63ysJ%2F7eCX2ObEpWNPJl1kRQsh5MFn%2BJttSR1blB5XMQpA9Yhrl8hg10GzkoNaSnNE%2B7sYKUrk%2BfaRZvRrwlpH6q1sXtMJFE3bzOseXLX7ZAqIsmrw8hjbxGO1EvPOn7JX7OyvvLmNxs3BsTw36YMbc4fDdEdd1OS9ZRVp%2Bs7QPPsFMlGFtbsXgsR765P%2BQasQlHn8G2CHnDDwNHLInrtIGx84FSkx3VveULhf4zMN4DsQfx81ZxdCWV3zwztQ%2F9cyB%2F6nL2R3lvx0JfMUeC5Ho0ijyom1OT%2BUfLYZLZDCwVbyjtMvoO%2FRGALlBquD10XrT7Rj3J0KEItgJ8X%2FmIVYk89YsPyNTiHXr2%2FS07TyCWdY%2Bcm3utu%2FJQm2w6Mn2oqGAcoVd1kJXfshEDRPz%2BYzi%2FezlR2FUOiSMKkEhSApKq5GhXQTnaLgDwWcx4bN7kCrDpXwjRiY8Iv5Q6Z5k6yU6aoZnpYoMlaG21aLjdhB%2F1yasi915ioWXR9CGCJm6Q9RFpsHIRZW1ps0gvZ7Gd%2B%2BWpK%2FeofSDr6rMycQYXuhv70fpRNbSxWofwySmzoi3KjgUtsIR08qlGOgSWhqGlyS8YrklbaWUhnd9mGK1kEfU%2FDBt6BI9t7yRK3g5DfT1gdoPHA1rhxl4AlN7XuSxa33a3R5SKcbDCJW%2BbLBIsYmh%2FQPjxj%2BkoCInoJHiFJWNq7cpZNwLv7RJg%2F%2F6eWzs%2F1UmcDZ5Id3gCpjlPHZ908Wrp%2FEjVGUvLQneYbAg0ZB7Ltgq4OelGxF6XhSdcwcx78KWLY4X%2BDcgN4WhED4TbRDEVJ8nI8UnbuWO8Tpk9UFUSMQBfjbtFxyw25fkNLisdfAE4%2B2ml9kyC96s50%2BADANCR5TEhMrkF9TDaPSGdVLSA4uQe0TCXiBFtbnJX%2Fes3To3JVVQLNCYpFbrvtapvBOhx7HMDl3mJqVmrXnXhkbezPEH%2B3GlutHRvvBcsXrcShaQNUfOI7%2FJWv2MySwZR2KBgLrNglLfmugihn71AvC1OHim5ODLgc%2BN0wPk9X8apSMGTUOh6IcuPIFYSnH5B0LhHDW0oZxbnU%2FjRydCVwpGCUTp0nU1fzsG3tsGMRvUdNh4FVal4ywqwzWFikC72eyx4R7qvBcEwaaLZo0Vhlf5%2FhV62aeOtLmH3XBvtQWNS5Q%2BVn6T9lyyP%2F%2FrC6ijr1iOMGWiwTS8GKE0ZhKCtf%2BVm3UA%2BGt7RyeOGZirlvgZXEB%2F1xx5Xxzw8uUVTxVUS9l7%2Fi%2BTuT4YMqAyEW5AMGnURfufz%2Bg87TixlCGrykJe9KXOaYw4voR3SrKlljzLSAg%2BiWDQhpF2Bh80BsJ7j%2B%2BynYwEW6iYBhsDjOITkKsrzHTiOMpODAloPaBR8WjBlPSsdtcK%2BOBm9iMgOb6fD8vLC28%2FKmEg1LrIs%2B4jrhbXfJxIpFlKGlYp1OBRMkJlMJ73vt4GjLXBK3t1gazTR84X7DjA805hARgOL%2FfTVBoBwXOd2e%2BJHRouSMms0o9608j0PoAAOdMmC3L5Jy7KuYvDHj2N%2BlpHe06QPG12EmVaPR03vwwkiGhvy5uatZigWO00WVQ%2FsJzWPUfNFhMcTlghWjv%2BiyyX97HV%2FxXlBjA%2FSSjfBQXP341CAzjNtka9W%2BiX2Bw8z92yIbaNQqLCh%2B9BYAhcCfN%2FXXHCPf%2B%2FoRmyaae%2BoHvtXHBbLry5hnJ9JaxiTW6k6fE%2FPnJ%2FQlopd%2FpoyOjYT2UHj7ivfeelg69VDys6U3fU3Oh6x%2FOttIZZwDkBN5dqKZGHa5RbZTapc5q3NyQ3BmK%2BHBf%2FAtUwRauhw7ytDlPt8jPBcywYTbTbiAY%2FR%2FWlTvIylRsxfUXaW5Js4g4QvGFNPeVj9be%2BPNKxAZbY2v%2FhXuJTWOw3sHMmHPKVnu70x8xXVeOTXGw4Jj0xoyTbrEwgXbdEOCz%2FWUlJyys3kZ80PkgqtLZZFUdbkA4w9WPqHr0AYonsCHdnK1SEUWn6g6lmXNM45%2Fij3c%2Fs7uHL2LrOLa8YTBxUaVGjDqjM1AK7xMwAQx%2F4okIRAtRU%2FXzUtxwjeLpB80NzxOrTGZwr8XV0zlX%2BbSo6cVBbvOim5TPsWW8Do6v8I%2BTrzKqfyZwMCmIWAjFXBGTXQ1vWHOh9sXAR2Yf86SUbZKKQXzmva7qvvcy7cbl1ptTUcsvG7yAVOLnUhvSwB7J6vlzEPm%2BRPdBRFp2HXQmw6LKijIlBqu4GnexQCtb5gecIlMrXoDH52CVBuZ3MuU4BrLQMmFdgo%2BeiSPHqPjUnK%2BjDxbTYVDt%2BDm8oSSlWpK1iPb7nwWyDIBFRqg9kkJkZBV6zNJX10Obs66fCBDmS%2FgINLNhLH%2BfoKg7nfKcwgnnOELs07LbtVILTU%2FXw8dWo%2B55qRUkYid2LUlE3z4ZGaK4zpOVseSeejo7xY6xJMDtpzpfE93%2FyHQ5%2FXBgp2fWxYYzX1dX9l9qm%2BvImKeGLLiT5cq3Owy%2FZSglfuWb%2FsoiW%2F9kkwz6KZhxDPICZuXKkWiI3A5GqaEleLOOMJ83KahTgcKem3tee%2BA6ydspVFagZGyEUNhBC0drxPRJng6AOwe2zDMIPwm3MeIHWFZeVLd8Pj%2BQHgMsHkC03aRfEoQggS0vOnJQOK8gxbClKS%2FjDBlQLE9Iit0J5UU%2BxRXOKVS4RZYNBgAZ%2BhMiCaG5uOiDh%2FM1f7c3mrd5JC%2F3b7rz6laDsxE9Tu2nAWUa6f3bo5SvHmOJEP9CDvUWi2DsOgF1yhG7xtw6reYrI2%2B4H106lqaK5nz2huDIF%2FFTS3O60TvPmF%2F04JC7jRATLNJiPOBjDmH3WObKA3OwhvfLlzldxrRTEpYnr05AK10A%2FEs3uabA%2BGnyD2Zv8lZnsq6eicOHH5gmQlnClOc9i7f13OdNk3h95WZW2FKwruBamLiAaEoGMZ5vXIu9ah%2FAOLPPMpfa7Ncc2Ast89AtRzU1zfQqwM2jZH7AjOoQqpuqKCZk%2FtxLyo9qO%2FfYAfMkHVTZb6qPUOldEPEOdSipDHLljM%2FrrnPOGgUJfSB%2F5Zh8r4L6n88DBYpVx35U0YXYbch33%2BMWRYc%2B3EA%2BZ%2FLWIk93SU1Dr15lp2Y3WyWB6iofQKiBmPflkn%2BcQqP%2FkT%2FPbhuFFn6fpDazIM6J2ix4r%2FlTuLDvZedi%2BR%2B0ZjPh9pCmIVgutBTr%2BmOtxafu8ns8dYtbwbMvRH8Z9qaqmv%2BwNLBreiTC7zR2pMngR9Qn8j5UJrG7p0oePF3gLX2srhxZ0L4kwH%2Fx2t05o9cdz6VDAn5T2o2lGJs%2BZpSkcasf5K5AyaF1hNVKdIaH%2FrF83FAcqZv%2BHavai5M%2F5znoji3jjwuewcDXE9S%2FnRo1B13s4QQ6MX4v9vxQsLsqz75DpXbZbRffEKMpNYuJrCeQP9JvXAZ9e8toyqG978iBudaEsgDyT7J5J16Lt4%2FaZ0js1uaZ5fQMQoLbSEIHF91cSgHhoA3WHOr%2B%2B0kJzIfAyNhwSsYY5EcAGG4RA0e9jH5af55QiHpfpokhxkBF2F5t9Y4UAvUe51aUkglAwnEDhySD4mNuijf4B31JwnYQZ6kL1x46I26rc0myiiFw%2FyQhExTZp6Pj3ydCWnMnEkl1xFxD63XDJfFlXq2othvtllSZ3P1tOqzMOloCDnzbFXHUpEDBBWgFX%2FK74tnY%2FzBBfa1X6seEabwLI%2FvdPxcl49GQwgz2oUUDLQTUV7TKd%2BD%2FDGg5k8S67Aw78DCwSuMJMHwlr4rS3YXCXxcAdjCQvqnEJAuZDbE7woeynfO9rYUGvwV9plfuMkWcmzYzdjin%2FSy%2FLnhbVCvaedFvklEMTNwsxpBF%2FEQ1FdrQ9Yy5A4ZcEcxv5E4dE6Ny5Ra%2BnLlirLR5ocP0r%2F5vSVTfqvsAKSSwzDWg%2BJr3t8njXIRI5UmUoJawawsQtVe8zjAu%2BUCDlzQKaSomEdd4icLfb1he6G9e5csL1zpnloFGzRyc6HGsakh9I8MvjNcIVsutPPOr6SjGz1%2Bz%2FDMShDMRhuKPt1PgmIeoi843ElxfQPCuJkR2Iy9WzJYk9eRei6rfppFmJfQt3KxK%2B5jgBXcCsQVur2M%2FyFrHrzzdDMBwk%2F8561jmOIB3qst7qMpri7lRDOD2YLXGnNVVADGBndYKQnXmRb5NV36G7gHUOHBjRTXnfiCrd6I2lBhq6PXExuW%2FFRApVvC1V8oeHq5r0p3fzzwkNR20YQ4Mi0IHJARGLTkSgXjKUvbuPOa2vo%2B5zzZiRha6mGoy937iq6AW1GPTk6tGkCZU%2F6JmWNC%2Bq4Lrvq%2FIVHWmSC6TvW1xqHsgrkwrLyY8hjB9iEHfkEV7FXqk8l6APKo7GLcUikbPGgJXHgAYJPPQjacRBUXR8XV0s49%2BQ1cgb9oYDOX14vX%2BeChJW5XBRAgXXGkSQ1J1MJOoJuYjQ%2BO0FvKAa6VIRWm3GYuS79psz2WJCv9NrIM82d3hRE1YIiCcb%2FEwrBtejpQzyCxBvqTFUIMoH2TnCSng0VRm60uIVLUrpmDN4T1S7HkWo1RjMXy9XBrPEJGV10Bbu2BjEiqsW%2FQJ3ou7KmGpEGBc4ZagvE4yYoHxPL3n2O7wpF4MZSeDLTD6vIlly29lIliUjpgbWhnHfDa%2BRJCWKjn0Q%2FYZZ%2FJx4m0npGJd2LAsGMS09ghztGYwwT9T5IfuIk1i3aVor8ptrRb8hJuPv1eJziXiqb8an908VztrMAz%2FQOt3Ev9kvpEMTIEZka%2F5YFwQ%2FONX%2Faw6MOxhTj4TmmApOdEF6qGv%2FELh%2BsMmPnhpz62w%2BpjZMYheyyT0Adj6NmVJkCBqhz%2B%2FeFt5CCoQKimXh3L%2F3ZDGbxk4%2BZOZrRLGGJ%2FuSVxDapB4uDc%2Be51alIcF6D6ka%2Bu9E%2FStiMa3JzsO%2FaB4UeXdoKkEGNC2WPUs2S9%2BzqynfAxVw3vMNYGr4E7WxTBIIIPmmBle0lgQ1mNyF3RvihmwY14RY2ziTMo2PrLSZ2pTi8fsrcjN%2B%2BiXcQu%2BX%2FFTj9EZuOwRV62kurtGojalWpIj%2FbbOjmDkWtLrSy5pXOdG%2FHkLx%2BLFXhZ8H%2FUGGWkFh%2BxBk%2ByP%2B4dOUibpkaXE5AzmnAMcauylfQPOaWprJNX6enBTk4sT%2FnudiMXMJB6T16DjSqbfbKXP%2Ft9I9IkWpt3yoHRPAFPv5zBrQFn09ulFqGFvY9oWTBa%2FZ8hEmpPS%2BIb7t2lbNshSKhTwn1pUI38CJqjWwB0Dwo4rSVN41x44ZMQbOFPtY8wjQ2urRF59iLcECJ43bQAhokaclpNwHSBCYo%2BZTFXIyCSs2pdMnq6VleYuJK6fb%2FBVm86x78g%2FHTcMMGfq5COAyC5ZtK%2Bj2UwSWhXK2ZI0LKEsg0T5Ge47F0hsds8iZDhctEQPVAzKWZ5F1PlicZw3DgtJhLBOHzc59y8dF%2FooCBx1cnXXbIyFA6hPaWGb1qdwQvfj9CenurJDmxSP37z7jwFQDqOZ9f4w24a2PZSNL79d0u3WWGnZTi6ZrlIZlJrW2R73PS0%2BrYiKLRzW%2B0xjeMgJa41jSwLOiMBK37fpj%2Btb8Xa9WhCxX1H9lexYFOVWEmyd%2FNDfS4Ct22xugsWEWpZjCSgJk%2B6EtDBingRl1gCR5e8xXQpEfRxYJob0yvJ%2FyxQIxUQYQpe%2Be%2BR4gUNVd2f1ioo5uoQWlrMAFHgbMejL2Tzc2jIKh7tnj%2BRvm%2FYnnK6Dq0ojzytUNOTPrqfAFoH4Obe79TN3dWixGYqhFS3UWgf9p%2FJslpSZkdaw0WYOH5LvJwOkSRQsTl59QTC0mwRuNHEnXkGbqFjN7FhIgLeH5PzvKQiHHYfemuO9K8OgLAorO5ZZIQhcwopAvZuL7nlphuVyxmHmOaUzld2fE2Sea4jI6iThmgaadB46xSiP%2B5Q%2F0KWWA2pG%2BIwAEeIysvTtRf7uotFdFbe%2FMTxb3N3L4SL%2BV8T4ZShVPxBori8zGvtyJBtt5w%2FJFuiVp7aEMaOcBtklf0dSMromLIIGqx5z4UiFfisMNmfF5eOHiYU9n8TBkc3mfvrWVBEEmbJYJ%2BLNt6lMm&__VIEWSTATEGENERATOR=F8CFDE04&__EVENTVALIDATION=vG%2Bo82GfSRQqI0N9waAOl2%2BeUBRtkjrxTLX68nlGjcsCKTESkT9Zyc6IzibnOlpDeFMNsWXRrQR8pmPhBRvh%2BrrKuVrT%2BFaoL1VQOMPT0b7kbw0NdgmnrTykWYAk2xABPaFMBaHANA%2FLDUX1d76znKh1rjRUmenxyHOTDqKnpH8hh3v7qfe%2BFvARCx7%2FPIpOHcVE2S%2FJ%2BdTaDv%2BPmOi3eUMY25doos%2Fos3FPQ1FPINEWqbIlWHOTzeiThDEOsMi9bFx5v181xsI6%2B4w0M%2F9kHF38%2BU%2FscBvE5jkDshvCvw%2FzRwhiMwk%2FxonWXYumX7eRqARYY8COceOUb8uk193%2BvJfOMbdhguLTVPmPe4rorA5sImGnY0zwtClwHrg9g9wub3tz8GjoKm6vQDRUGK598tBrMd98gMuKCXDxmWLGSas%2BporLOV3hoTgVUGPJ6Ah6UZhxi%2BeLNvB3BTA2KIlMvlHFzi0fS0vu2rAMGRtU5v%2BZjLk1YuxedYsazSUlmPAEsnVSecxRIsSPYmONBGuXGeO2Cc%2BgEtwzgs8U4EgV8eJIDYj3vYqJA9rUfI%2Bc6E6o29YFGxh2w2ryZfc3wyO5a%2FJYTTRx5pADnfPQC8V8i5yJKJVaRKM3UfTTxPINJ8H0P%2FxUdQre%2FgR25rTmCzg3QN1aO8owTTLGQxjsURCuzQdj1vF1ULVT7jKfdhfjgI8XkbeQEDTxeQjz0Ug58gZjQIszjW6eQES3diYnIaYeMrQNGIhBYj2nZ%2F9j4LUeLXyCIZ7B97SRzTSnPGZ7f8hReEmvR8aau0eQXCy3xODfhUhZ2%2F5gxGD16IsVTnpMNjURwAQanc0UG7HlpUV8bHLhFJ5rXs0Qc1v8nQiCdR6il44UPcGoUb760XsB1QDJwdT8aQfwo%2FuxnpnjtgCd964T74u9%2B7sAMoE%2FmPhvtK2dy3HZevHjBrKjmQtd4Xw3xIkosI1OfE%2BtNDZuWavReMVkQ8Yt2HIEJQll1XVfXkc3sS8otSxeRNy3HcTvu4YD8ORrDsgpwvOdhSW9zCukJpfR2O18Ahlc4OkHNKmUD%2FNV%2BOGmJe5W%2Fn1lC%2B19oXFoa5tF3skayjUOtpG43BmRCp6IkTaPcPioRjew67HzvxBBmcTkIgZWGByANSpXZsgscPO8s0KW5UmKtcU6WkFsMm1XGdwWYSQ24z74BFOG3HulPmfer6KrVebBB59j0gCVs%2FyMbn3VTA%3D%3D&ctl00%24tbCompanySearch=&ctl00%24MainContent%24sfMessageType%24txtObjectName=%D0%A1%D0%BE%D0%BE%D0%B1%D1%89%D0%B5%D0%BD%D0%B8%D0%B5+%D0%BE+%D0%B2%D1%8B%D0%BF%D1%83%D1%81%D0%BA%D0%B5+%D0%BD%D0%B5%D0%B7%D0%B0%D0%B2%D0%B8%D1%81%D0%B8%D0%BC%D0%BE%D0%B9+%D0%B3%D0%B0%D1%80%D0%B0%D0%BD%D1%82%D0%B8%D0%B8&ctl00%24MainContent%24sfMessageType%24hfIdObject=IssueIndependentGuarantee&ctl00%24MainContent%24sfMessageType%24hfAdditionalInfo=&ctl00%24MainContent%24cbShowForeignSystemMessages=on&ctl00%24MainContent%24sfCompanySelector%24txtObjectName=&ctl00%24MainContent%24sfCompanySelector%24hfIdObject=&ctl00%24MainContent%24sfCompanySelector%24hfAdditionalInfo=&ctl00%24MainContent%24sfIndividualEntrepreneur%24txtObjectName=&ctl00%24MainContent%24sfIndividualEntrepreneur%24hfIdObject=&ctl00%24MainContent%24sfIndividualEntrepreneur%24hfAdditionalInfo=&ctl00%24MainContent%24sfAppraiser%24txtObjectName=&ctl00%24MainContent%24sfAppraiser%24hfIdObject=&ctl00%24MainContent%24sfAppraiser%24hfAdditionalInfo=&ctl00%24MainContent%24sfPerson%24txtObjectName=&ctl00%24MainContent%24sfPerson%24hfIdObject=&ctl00%24MainContent%24sfPerson%24hfAdditionalInfo=&ctl00%24MainContent%24sfNonResidentCompany%24txtObjectName=&ctl00%24MainContent%24sfNonResidentCompany%24hfIdObject=&ctl00%24MainContent%24sfNonResidentCompany%24hfAdditionalInfo=&ctl00%24MainContent%24dpBeginPublishDate%24txtDate=01.01.2018&ctl00%24MainContent%24dpEndPublishDate%24txtDate=&ctl00%24MainContent%24tbMessageNumber=&ctl00%24MainContent%24btnSearch=%D0%9F%D0%BE%D0%B8%D1%81%D0%BA&ctl00%24MainContent%24ucMonitoringControl%24txtEmail=&ctl00%24MainContent%24ucMonitoringControl%24txtPassword='

#data={'ctl00$MainContent$ucBottomDataPager$ctl00$ctl00':''}

df=pd.DataFrame()
session=requests.Session()
res1=session.post(url1,headers=head1,data=data)
print(res1)
res2=session.get(url2,headers=head2)
print(res2)
soup=BeautifulSoup(res2.text,'lxml')
div=soup.find('div',{'id':'ctl00_MainContent_ctl12'})
links=div.find_all('div',{'class':'listItem'})
for i,link in enumerate(links):
    sss=None
    print(i)
    msg_url='https://se.fedresurs.ru'+link['onclick'][len(" window.location.assign('"):link['onclick'].find("');")]
    msg=session.get(msg_url,headers=msg_head)
    msg_soup=BeautifulSoup(msg.text,'lxml')
    try:
        substr1=msg_soup.find('div',{'id':'content'}).find('td',{'data-element-type':'page-content'}).find('div').find_all('div')[0].text.replace('\n',' ').replace('\r',' ').replace('\xa0',' ').replace('№','').strip()
        df=df.set_value(i,'Номер',substr1.split()[1])
        df=df.set_value(i,'Дата публикации',substr1.split()[3])
    except:
        pass
    try:
        trs=msg_soup.find('div',{'id':'content'}).find('td',{'data-element-type':'page-content'}).find('div').find_all('div')[4].find_all('tr')
        try:
            df=df.set_value(i,'Тип сообщения',[ss for ss in trs[0].text.strip().split('  ') if ss!=''][1])
        except:
            pass
        try:
            df=df.set_value(i,'Гарант',[ss for ss in trs[1].text.strip().split('  ') if ss!=''][1])
        except:
            pass
        try:
            sss=[ss for ss in trs[1].text.strip().split('  ') if ss!=''][2]
        except:
            pass
        else:
            try:
                df=df.set_value(i,'Гарант_ИНН',sss[len('(ИНН: '):sss.find(',')])
            except:
                pass
            try:
                df=df.set_value(i,'Гарант_ОГРН',sss[sss.find(',')+len(' ОГРН: '):sss.find(')')].strip())
            except:
                pass
        try:
            df=df.set_value(i,'Принципал',[ss for ss in trs[2].text.strip().split('  ') if ss!=''][1])
        except:
            pass
        try:
            sss=[ss for ss in trs[2].text.strip().split('  ') if ss!=''][2]
        except:
            pass
        else:
            try:
                df=df.set_value(i,'Принципал_ИНН',sss[sss.find(', Аналог ИНН: ')+len(', Аналог ИНН: '):sss.find(')')])
            except:
                try:
                    df=df.set_value(i,'Принципал_ИНН',sss[len('(ИНН: '):sss.find(',')])
                except:
                    pass
                try:
                    df=df.set_value(i,'Принципал_ОГРН',sss[sss.find(',')+len(' ОГРН: '):sss.find(')')].strip())
                except:
                    pass
        try:
            df=df.set_value(i,'Бенефициар',trs[6].find('td').text)
        except:
            pass
        try:
            sss=trs[6].find_all('td')[1].text.split()
        except:
            pass
        else:
            if 'Аналог' in sss:
                df=df.set_value(i,'Бенефициар_ИНН',sss[-1])
            else:
                try:
                    df=df.set_value(i,'Бенефициар_ИНН',sss[1])
                except:
                    pass
                try:
                    df=df.set_value(i,'Бенефициар_ОГРН',sss[3])
                except:
                    pass
        try:
            df=df.set_value(i,'Номер гарантии',trs[8].find_all('td')[1].text)
        except:
            pass
        try:
            df=df.set_value(i,'Дата выдачи',trs[9].find_all('td')[1].text)
        except:
            pass
        try:
            df=df.set_value(i,'Дата начала действия',trs[10].find_all('td')[1].text)
        except:
            pass
        try:
            df=df.set_value(i,'Дата завершения действия',trs[11].find_all('td')[1].text)
        except:
            pass
        try:
            df=df.set_value(i,'Ссылка на торги на ЭТП',trs[13].find_all('td')[1].text)
        except:
            pass
        try:
            df=df.set_value(i,'Описание основного обязательства',trs[14].find_all('td')[1].text)
        except:
            pass
        try:
            df=df.set_value(i,'Сумма',trs[16].find_all('td')[1].text)
        except:
            pass
        try:
            df=df.set_value(i,'Неизменяемая сумма',trs[17].find_all('td')[1].text)
        except:
            pass
        try:
            df=df.set_value(i,'Ссылка',link['onclick'][len(" window.location.assign('"):link['onclick'].find("');")])
        except:
            pass
    except:
        pass
    