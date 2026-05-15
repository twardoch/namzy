// this_file: namzy-cpp/src/namzy.cpp
#include "namzy.h"
#include "wordlist.h"
#include "mangle.h"

#include <QNetworkAccessManager>
#include <QNetworkRequest>
#include <QNetworkReply>
#include <QEventLoop>
#include <QTimer>
#include <QJsonDocument>
#include <QJsonArray>
#include <QUrl>

Namzy::Namzy(quint64 seed)
    : m_rng(seed)
{
}

QString Namzy::capitalize(const QString& s)
{
    if (s.isEmpty()) return s;
    return s.at(0).toUpper() + s.mid(1).toLower();
}

QString Namzy::pickWord(const char* const* words, int count)
{
    int idx = static_cast<int>(m_rng.bounded(static_cast<quint32>(count)));
    return QString::fromLatin1(words[idx]);
}

QString Namzy::fuse(const QString& geo, const QString& common)
{
    const QString fused = joinClean(geo.toLower(), common.toLower());
    const QString mangled = mangle(fused);
    return capitalize(mangled);
}

QString Namzy::generateOffline()
{
    QString geo    = pickWord(Wordlist::GEO_WORDS,    Wordlist::GEO_COUNT);
    QString common = pickWord(Wordlist::COMMON_WORDS, Wordlist::COMMON_COUNT);
    return fuse(geo, common);
}

QString Namzy::generateOnline()
{
    QNetworkAccessManager manager;
    QNetworkRequest request(QUrl(QStringLiteral(
        "https://random-word-api.herokuapp.com/word?number=2&length=6")));
    request.setTransferTimeout(3000);

    QEventLoop loop;
    QTimer timeout;
    timeout.setSingleShot(true);
    timeout.setInterval(3000);

    QNetworkReply* reply = manager.get(request);

    QObject::connect(reply,    &QNetworkReply::finished, &loop, &QEventLoop::quit);
    QObject::connect(&timeout, &QTimer::timeout,         &loop, &QEventLoop::quit);

    timeout.start();
    loop.exec();
    timeout.stop();

    auto isAlpha = [](const QString& s) {
        for (const QChar& c : s)
            if (!c.isLetter() || c.unicode() > 127) return false;
        return !s.isEmpty();
    };

    if (reply->error() == QNetworkReply::NoError) {
        QByteArray data = reply->readAll();
        reply->deleteLater();

        QJsonDocument doc = QJsonDocument::fromJson(data);
        if (doc.isArray()) {
            QJsonArray arr = doc.array();
            if (arr.size() >= 2) {
                QString w1 = arr.at(0).toString();
                QString w2 = arr.at(1).toString();
                if (isAlpha(w1) && isAlpha(w2)) {
                    return fuse(w1, w2);
                }
            }
        }
    } else {
        reply->deleteLater();
    }

    return generateOffline();
}
