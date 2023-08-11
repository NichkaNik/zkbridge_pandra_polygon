Нужно самостоятельно дернуть кран в тестовый БНБ

https://testnet.bnbchain.org/faucet-smart

Вставляем один приватник в <b>conf.py</b>

Сначала бриджим тестовый БНБ в opBNB и Combo

<b>bridge_bnb.py</b> бриджит по половине депозита поровну в обе сети (в opBNB комса скачет до конских значений, бридж с запасом на комсу)

<b>minter.py</b> минтит 6 нфт панд в Полигоне и создает тестовик кошелек_IDs.txt с айдишками сминченных НФТ

<b>polygon.py</b> аппрувит и бриджит 

Делаем бриджи 6 нфт панд из полигона в следующей последовательности:
<ul>
<li>Polygon - opBNB Testnet </li>
<li>Polygon - Mantle (LZ)</li>
<li>Polygon - Core Dao (LZ)</li>
<li>Polygon - Combo Testnet</li>
<li>Polygon - BNB Chain (LZ)</li>
<li>Polygon - Celo (LZ)</li>
</ul>

opBNB и Combo не через LZ - создается кошелек_hashes.txt, в которые летят хеши обеих транз, они нужны для будущего клейма

Слипы выставлены слишком большими, можно офигеть ждать.

В конце нужно склеймить свои бриджнутые НФТ в opBNB и Combo

<b>claim.py</b> - после бриджа лучше подождать какое то время, сети как то не всегда с первого раза дают клеймить и часто тупят

<h2>Либы для установки</h2>

pip install web3

pip install fake-useragent

<h2>Для запуска</h2>

python3 bridge_bnb.py

python3 minter.py

python3 polygon.py

python3 claim.py


*Сорри за говнокод
