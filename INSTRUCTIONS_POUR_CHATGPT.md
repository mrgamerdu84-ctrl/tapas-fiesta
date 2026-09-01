# Instructions pour générer l'APK Android — Tapas Fiesta!

Bonjour ChatGPT 👋 (ou tout autre assistant qui reprend ce projet).

Ce zip contient un projet **Capacitor** prêt à être transformé en APK Android autonome.
L'application est un jeu de cartes/plateau 100% autonome écrit en HTML/CSS/JS vanilla
(aucune dépendance réseau — musique et images sont déjà intégrées en base64 dans le fichier).
Capacitor sert uniquement à l'emballer dans une coquille Android native (WebView).

## Contenu du zip

```
tapas-capacitor/
├── www/
│   └── index.html          ← le jeu complet (HTML/CSS/JS + musique embarquée)
├── package.json            ← dépendances npm (Capacitor)
├── capacitor.config.json   ← configuration Capacitor (nom de l'app, appId, etc.)
├── .github/workflows/
│   └── build-apk.yml       ← pipeline GitHub Actions qui build l'APK automatiquement
├── .gitignore
└── INSTRUCTIONS_POUR_CHATGPT.md  ← ce fichier
```

Le dossier `android/` n'existe pas encore : il est généré automatiquement à l'étape
`npx cap add android` (voir plus bas), que ce soit en local ou via CI. Il n'a pas besoin
d'être fourni à l'avance.

## Option A — Le plus simple : GitHub Actions (recommandé, aucune installation)

Cette option ne nécessite ni Android Studio ni SDK installés quelque part : tout se
construit dans le cloud, gratuitement, sur les serveurs de GitHub.

1. Crée un nouveau dépôt GitHub (public ou privé), par exemple `tapas-fiesta-app`.
2. Pousse tout le contenu de ce zip à la racine du dépôt :
   ```bash
   git init
   git add .
   git commit -m "Initial commit - Tapas Fiesta Capacitor project"
   git branch -M main
   git remote add origin https://github.com/<ton-compte>/tapas-fiesta-app.git
   git push -u origin main
   ```
3. Va dans l'onglet **Actions** du dépôt sur GitHub. Le workflow "Build Android APK"
   se lance automatiquement au push (ou lance-le manuellement via le bouton
   "Run workflow" si besoin — il est aussi déclenché par `workflow_dispatch`).
4. Une fois le workflow terminé (2-5 minutes), ouvre le run terminé → section
   **Artifacts** en bas de page → télécharge `tapas-fiesta-apk-debug.zip`.
5. Dézippe : à l'intérieur se trouve `app-debug.apk`, installable directement sur
   un téléphone Android (il faudra autoriser "Sources inconnues" dans les
   paramètres Android pour l'installer, car l'APK n'est pas signé pour le Play Store).

C'est un **APK de debug**, parfait pour tester sur un téléphone ou le partager
directement. Pour une publication sur le Play Store, voir la section signature
plus bas.

## Option B — En local (si tu as déjà Node.js + Android Studio / SDK)

```bash
cd tapas-capacitor
npm install
npx cap add android
npx cap sync android
cd android
./gradlew assembleDebug
```

L'APK généré se trouve dans :
`android/app/build/outputs/apk/debug/app-debug.apk`

Tu peux aussi ouvrir le dossier `android/` directement dans **Android Studio**
(`File > Open`) si tu préfères builder ou déboguer depuis l'IDE plutôt qu'en
ligne de commande.

## Prérequis techniques (si build en local)

- Node.js 18+ et npm
- JDK 17 (Temurin recommandé)
- Android SDK (via Android Studio, ou juste les command-line tools)
- Variable d'environnement `ANDROID_HOME` / `ANDROID_SDK_ROOT` configurée

Si l'une de ces briques manque, préfère l'**Option A** (GitHub Actions) qui
s'occupe de tout automatiquement dans un environnement déjà configuré.

## Pour publier sur le Google Play Store (au-delà du simple test)

L'APK produit ci-dessus est un APK de **debug**, non signé pour la distribution.
Pour publier réellement sur le Play Store, il faut :

1. Générer une clé de signature :
   ```bash
   keytool -genkey -v -keystore tapas-release.keystore -alias tapas -keyalg RSA -keysize 2048 -validity 10000
   ```
2. Configurer `android/app/build.gradle` avec les infos de signature (`signingConfigs`).
3. Construire un bundle de release :
   ```bash
   cd android
   ./gradlew bundleRelease
   ```
   Le fichier `.aab` (Android App Bundle) généré est celui à uploader sur la
   Google Play Console (pas l'APK — Google demande le format `.aab` désormais).

Cette étape est optionnelle : si le but est juste de tester le jeu sur un ou
plusieurs téléphones, l'APK de debug de l'Option A suffit amplement.

## Personnalisation optionnelle

- **Nom de l'app / icône** : modifiable dans `capacitor.config.json` (`appName`)
  et via `npx cap add android` qui génère des icônes par défaut dans
  `android/app/src/main/res/` — remplaçables par tes propres images si tu veux
  une icône personnalisée (`mipmap-*` folders).
- **appId** (`com.tapasfiesta.app`) : à changer si tu comptes publier sur le
  Play Store, car il doit être unique globalement.

## Notes sur le contenu de l'app elle-même

- Le fichier `www/index.html` est un jeu complet et autonome (règles, roue
  interactive, mode solo contre IA et mode passe-et-joue à deux, musique de
  fond, effets sonores synthétisés en JS). Il ne nécessite aucune connexion
  réseau pour fonctionner — tout est embarqué (y compris la musique en base64).
- Si des modifications du jeu sont nécessaires, elles se font directement dans
  `www/index.html`, puis il suffit de relancer `npx cap sync android` (ou de
  repousser sur GitHub pour relancer le build automatique) pour les répercuter
  dans l'APK.

Bon build ! 🌮🎲
