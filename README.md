# Warcaby

  Zasady bicia obowiązujące w grze: Jeśli pion może wykonać bicie, to musi to zrobić, jednak nie jest konieczne ruszanie nim. Jeśli możliwe jest bicie większe niż pojedyncze, to nie można przestać zbijać w trakcie (np. po dwóch biciach w możliwym potrójnym).

  Działanie programu:
1. Przy kliknięciu na szachownicę program sprawdza, czy żadna figura nie jest obecnie trzymana (held_piece). Jeśli nie, to held_piece staje sie klikniętą figurą. Następnie, za pomocą metody check_possible_moves, obliczane są pola, na które figura ta może się ruszyć. Jeżeli jednak held_piece nie jest puste, przy kliknięciu na szachownicę program rusza figurą, jeśli jest to dozwolone według zasad. W tym samym miejscu sprawdza też, czy możliwe jest podwójne bicie (double_capture). W przypadku kliknięcia na figurę tego samego koloru, held_piece jest zmieniany właśnie na nią, a możliwe ruchy obliczane są od nowa. 
2. Po ruchu program sprawdza, czy żadne z pionów nie znajduję się na końcowej linii, a jeśli tak, to zmienia go w damkę (promote()).
3. Jeśli nie ma na szachownicy figur jednego z graczy, gra kończy się i wyświetlany jest komunikat informujący o zwycięzcy.
4. Dalsza część programu to głównie zaznaczanie trzymanej figury, dostępnych ruchów itp.

![1](https://user-images.githubusercontent.com/81564842/167607463-7cb6e352-933c-47ef-972f-165cc238a998.PNG)
![2](https://user-images.githubusercontent.com/81564842/167607502-9604c241-b005-4866-bd52-ef70d6ba2b35.PNG)
![3](https://user-images.githubusercontent.com/81564842/167607528-3916a790-0e03-4335-b4e7-18ad531f8d1a.PNG)
