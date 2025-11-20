import java.util.*;

public class HeuristicQueryWriter implements QueryWriter {

	private final List<String> stopwords;
	private final List<String> suffixList;
    private final Map<Intent, List<String>> boosters;
    private static final int MAX_TERMS = 10;

    public HeuristicQueryWriter(List<String> stopwords, Map<Intent, List<String>> boosters, List<String> suffixList) {
        this.stopwords = stopwords;
        this.boosters = boosters;
        List<String> tempSuffixList = new ArrayList<>(suffixList);
        tempSuffixList.sort((s1, s2) -> s2.length() - s1.length());
		this.suffixList = tempSuffixList;
    }
    @Override
    public List<String> write(String question, Intent intent) {
        if (question == null || question.isEmpty()) {
            return Collections.emptyList();
        }
        
        
        // Lowercase all, Split each term, delete unnecessary punctuation
        String[] splitTerms = question.toLowerCase().replaceAll("[^\\wçÇğĞıİöÖşŞüÜ\\s]", " ").split("\s+");

        
        
        //create our terms list, first stem the terms than add them to list excluding stopwords
        List<String> terms = new ArrayList<>();
        for (String term : splitTerms) {
        	boolean isCore = true;
        	while(isCore)
        	{
        		isCore = false;
        		for (String suffix : suffixList) {
            		if (term.endsWith(suffix)) {
        				term = term.substring(0, term.length()-suffix.length());
                		isCore = true;
                		break;
        			}
            	}
        	}
        	
            
            if (!term.isEmpty() && !stopwords.contains(term) && !terms.contains(term) && terms.size() < MAX_TERMS) {
            	terms.add(term);
            }
        }
        
        

        //add terms that comes with intent, they have priority
        List<String> boosterTerms = boosters.getOrDefault(intent, Collections.emptyList());
        
        for (String boosterTerm : boosterTerms) {
        	if (terms.contains(boosterTerm))
        			terms.remove(boosterTerm);
    		terms.add(0, boosterTerm);
    		if(terms.size() >= MAX_TERMS)
    			terms.remove(MAX_TERMS);
        }

        return terms;
    }
}