curl http://crypto.praetorian.com/challenge/2/ -H "Authorization":"" |  python3 -c "import sys, json; print(json.load(sys.stdin)['challenge'])" | cut -c 23- | base64 --decode > prae.png; pngsplit prae.png; cat *HCKR;

curl http://crypto.praetorian.com/challenge/2/ -H "Authorization":"" -H "Content-Type":"application/json" -d '{"guess":""}';
