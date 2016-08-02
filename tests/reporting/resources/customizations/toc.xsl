<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="2.0"
                xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                xmlns:outline="http://wkhtmltopdf.org/outline"
                xmlns="http://www.w3.org/1999/xhtml">
    <xsl:output doctype-public="-//W3C//DTD XHTML 1.0 Strict//EN"
                doctype-system="http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd"
                indent="yes"/>
    <xsl:template match="outline:outline">
        <html>
            <head>
                <title>Table of Contents</title>
                <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
                <style>
                    h1 {
                    text-align: left;
                    font-size: 20px;
                    font-family: "Liberation Sans", "serif";
                    color: #2981C4;
                    font-weight: bold;
                    margin-left: 1em;
                    }
                    div {border-bottom: 1px dotted rgb(200,200,200);}
                    span {float: right;}
                    li {list-style: none;}
                    ul {
                    font-size: 14px;
                    font-family: "Liberation Serif", "serif";
                    }
                    ul {padding-left: 0em;}
                    ul ul {padding-left: 3em;}
                    a {text-decoration:none; color: black;}
                </style>
            </head>
            <body>
                <h1>Table of Contents</h1>
                <ul>
                    <xsl:apply-templates select="outline:item/outline:item">
                        <xsl:with-param name="i" select="0"/>
                    </xsl:apply-templates>
                </ul>
            </body>
        </html>
    </xsl:template>
    <xsl:template match="outline:item">
        <xsl:param name="i"/>
        <xsl:if test="$i &lt; 2 and @page &gt; 2"><!-- TOC depth 2 AND remove TOC from the TOC :) which is on page 2 -->
            <li>
                <xsl:if test="@title!=''">
                    <div>
                        <a>
                            <xsl:if test="@link">
                                <xsl:attribute name="href">
                                    <xsl:value-of select="@link"/>
                                </xsl:attribute>
                            </xsl:if>
                            <xsl:if test="@backLink">
                                <xsl:attribute name="name">
                                    <xsl:value-of select="@backLink"/>
                                </xsl:attribute>
                            </xsl:if>
                            <xsl:value-of select="@title"/>
                        </a>
                        <span>
                            <xsl:value-of select="@page"/>
                        </span>
                    </div>
                </xsl:if>
                <ul>
                    <xsl:comment>added to prevent self-closing tags in QtXmlPatterns</xsl:comment>
                    <xsl:apply-templates select="outline:item">
                        <xsl:with-param name="i" select="$i+1"/>
                    </xsl:apply-templates>
                </ul>
            </li>
        </xsl:if>
    </xsl:template>
</xsl:stylesheet>
