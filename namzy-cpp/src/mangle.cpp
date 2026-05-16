// this_file: namzy-cpp/src/mangle.cpp
#include "mangle.h"

struct RotationRule
{
    ushort from;
    ushort to;
};

static const RotationRule ROTATION_RULES[] = {
    { 'c', 'q' },
    { 'f', 'v' },
    { 'k', 'c' },
    { 'q', 'k' },
    { 's', 'z' },
    { 'z', 's' },
    { 'v', 'f' },
    { 'w', 'u' },
    { 'b', 'p' },
    { 'p', 'b' },
};

quint16 allRotationRules()
{
    return static_cast<quint16>((1U << (sizeof(ROTATION_RULES) / sizeof(ROTATION_RULES[0]))) - 1U);
}

static QChar rotateConsonant(QChar ch, quint16 activeMask)
{
    const bool upper = ch.isUpper();
    const QChar lo = ch.toLower();
    const ushort code = lo.unicode();
    for (int i = 0; i < static_cast<int>(sizeof(ROTATION_RULES) / sizeof(ROTATION_RULES[0])); ++i) {
        if ((activeMask & (1U << i)) != 0 && code == ROTATION_RULES[i].from) {
            const QChar out(ROTATION_RULES[i].to);
            return upper ? out.toUpper() : out;
        }
    }
    return ch;
}

QString mangle(const QString& word, quint16 activeMask)
{
    QString result;
    result.reserve(word.size());
    for (const QChar& c : word) {
        result.append(rotateConsonant(c, activeMask));
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
