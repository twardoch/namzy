// this_file: namzy-cpp/src/namzy.cpp
#include "namzy.h"
#include "wordlist.h"
#include "mangle.h"


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

QString Namzy::generate()
{
    QString geo    = pickWord(Wordlist::GEO_WORDS,    Wordlist::GEO_COUNT);
    QString common = pickWord(Wordlist::COMMON_WORDS, Wordlist::COMMON_COUNT);
    if (m_rng.bounded(2) == 0) {
        return fuse(geo, common);
    }
    return fuse(common, geo);
}
