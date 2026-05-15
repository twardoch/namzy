// this_file: namzy-cpp/src/mangle.cpp
#include "mangle.h"

static QChar rotateConsonant(QChar ch)
{
    const bool upper = ch.isUpper();
    const QChar lo = ch.toLower();
    QChar out = lo;
    switch (lo.unicode()) {
    case 'c': out = QChar('q'); break;
    case 'f': out = QChar('v'); break;
    case 'k': out = QChar('c'); break;
    case 'q': out = QChar('k'); break;
    case 's': out = QChar('z'); break;
    case 'z': out = QChar('s'); break;
    case 'v': out = QChar('f'); break;
    case 'w': out = QChar('u'); break;
    default: return ch;
    }
    return upper ? out.toUpper() : out;
}

QString mangle(const QString& word)
{
    QString result;
    result.reserve(word.size());
    for (const QChar& c : word) {
        result.append(rotateConsonant(c));
    }
    return result;
}

static bool isVowel(QChar c)
{
    switch (c.toLower().unicode()) {
    case 'a': case 'e': case 'i': case 'o': case 'u': case 'y':
        return true;
    default:
        return false;
    }
}

QString joinClean(const QString& a, const QString& b)
{
    QString head = a;
    QString tail = b;
    for (int pass = 0; pass < 2; ++pass) {
        if (head.isEmpty() || tail.isEmpty()) break;
        const QChar last = head.at(head.size() - 1);
        const QChar first = tail.at(0);
        if (last == first) {
            tail.remove(0, 1);
        } else if (isVowel(last) && isVowel(first)) {
            tail.remove(0, 1);
        } else {
            break;
        }
    }
    return head + tail;
}
